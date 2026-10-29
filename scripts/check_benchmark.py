# Copyright (c) Meta Platforms, Inc. and affiliates.
# SPDX-License-Identifier: CC-BY-NC-4.0

import hashlib
import json
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'benchmark'
inputs = [json.loads(line) for line in (root / 'inputs.jsonl').read_text().splitlines()]
golden = [json.loads(line) for line in (root / 'golden.jsonl').read_text().splitlines()]
assert len(inputs) == len(golden) == 604
input_ids = [row['id'] for row in inputs]
golden_ids = [row['id'] for row in golden]
assert len(set(input_ids)) == 604 and set(input_ids) == set(golden_ids)
by_id = {row['id']: row for row in golden}
references = set()
for row in inputs:
    answer = by_id[row['id']]
    for key in ('n', 'k', 'level', 'held_out'):
        assert row[key] == answer[key], (row['id'], key)
    for arm in row['arms'].values():
        digest = hashlib.sha256(arm['prompt_text'].encode()).hexdigest()
        assert digest.startswith(arm['prompt_sha']), row['id']
        for image in arm['images']:
            path = Path(image)
            assert not path.is_absolute() and '..' not in path.parts
            references.add(image)

# Each tuple gives (right axis, right sign, up axis, up sign, depth axis, depth sign).
axes = {
    '+X': (1, 1, 2, 1, 0, 1), '-X': (1, -1, 2, 1, 0, -1),
    '+Y': (0, -1, 2, 1, 1, 1), '-Y': (0, 1, 2, 1, 1, -1),
    '+Z': (0, 1, 1, 1, 2, 1), '-Z': (0, -1, 1, 1, 2, -1),
}
for row in golden:
    n = row['n']
    volume = row['structure_3d']
    assert len(volume) == n and all(len(layer) == n for layer in volume)
    assert all(len(line) == n for layer in volume for line in layer)
    ra, rs, ua, us, da, ds = axes[row['held_out']]
    grid = [['.'] * n for _ in range(n)]
    depths = [[-n - 1] * n for _ in range(n)]
    actual_pieces = {}
    for z in range(n):
        for y in range(n):
            for x in range(n):
                letter = volume[z][y][x]
                if letter == '.':
                    continue
                point = (x, y, z)
                actual_pieces.setdefault(letter, set()).add(point)
                col = point[ra] if rs == 1 else n - 1 - point[ra]
                up = point[ua] if us == 1 else n - 1 - point[ua]
                line = n - 1 - up
                depth = ds * point[da]
                if depth > depths[line][col]:
                    grid[line][col] = letter
                    depths[line][col] = depth
    assert actual_pieces == {k: {tuple(p) for p in v} for k, v in row['pieces'].items()}
    projected = [''.join(line) for line in grid]
    assert projected == row['answer_grid'], row['id']
    expected = row['expected_output']
    if isinstance(expected, str):
        expected = json.loads(expected)
    assert expected['answer'] == projected, row['id']

assert len(references) == 11634
print('Validated 604 paired examples, all prompt hashes, piece coordinates, and ray-cast answers.')
if '--metadata-only' not in sys.argv:
    actual_images = {str(path.relative_to(root)) for path in (root / 'images').rglob('*.png')}
    assert actual_images == references, (len(actual_images), len(references), list(references - actual_images)[:5])
    total = 0
    maximum = 0
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        size = path.stat().st_size
        assert size < 100 * 1024 * 1024, path
        total += size
        maximum = max(maximum, size)
        if path.suffix == '.png':
            with path.open('rb') as f:
                header = f.read(24)
            assert header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR', path
            assert all(struct.unpack('>II', header[16:24])), path
    print(f'Validated {len(actual_images):,} PNG references and headers. Total {total:,} bytes; largest file {maximum:,} bytes.')
