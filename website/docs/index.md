---
id: index
title: SixthView Benchmark
slug: /
---

SixthView evaluates spatial reasoning by asking models to predict a withheld
face of a block assembled from interlocking cube pieces.

## Download

```bash
git clone https://github.com/facebookresearch/sixthview_benchmark.git
```

The repository includes 604 examples and 11,634 PNGs.

| Path | Contents |
| --- | --- |
| `benchmark/inputs.jsonl` | Model inputs for four arms: text, multiple images, text with multiple images, and a single image |
| `benchmark/golden.jsonl` | 3D structures, held-out faces, and expected answers |
| `benchmark/images/` | Images referenced by the inputs |

Resolve image paths relative to `benchmark/` and join the two JSONL files by
`id`. Score the predicted `answer` against the expected answer. The held-out
face image is a placeholder, so the inputs do not reveal the answer.

See the [repository README](https://github.com/facebookresearch/sixthview_benchmark#readme)
for the complete data format and face-axis conventions.

## Validate

From the repository root, with Python 3.10 or newer:

```bash
python scripts/check_benchmark.py
```

The validation checks example IDs, prompt hashes, image references, PNG headers,
piece coordinates, and answers computed from the 3D structures.

## Contribute

Read the
[contribution guide](https://github.com/facebookresearch/sixthview_benchmark/blob/main/CONTRIBUTING.md)
and
[Code of Conduct](https://github.com/facebookresearch/sixthview_benchmark/blob/main/CODE_OF_CONDUCT.md).

## License

Copyright (c) Meta Platforms, Inc. and affiliates.

The repository is licensed under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
Sharing and adaptations require attribution, an indication of changes, and
noncommercial use. See the
[full license](https://github.com/facebookresearch/sixthview_benchmark/blob/main/LICENSE).
