# SixthView Benchmark

| file | rows | what |
|---|---|---|
| `benchmark/inputs.jsonl` | 604 | the exact model input for every arm, keyed by `id` |
| `benchmark/golden.jsonl` | 604 | the real 3D structure and the expected model output, keyed by `id` |
| `benchmark/images/<id>/` | 11,634 PNGs | every image referenced by `inputs.jsonl` |

## Usage

Clone this repository to download the benchmark:

```bash
git clone https://github.com/facebookresearch/sixthview_benchmark.git
```

Read `benchmark/inputs.jsonl` and resolve its image paths relative to `benchmark/`.
Join examples with `benchmark/golden.jsonl` by `id` for evaluation.

## inputs.jsonl

```
id, n, k, level, held_out
arms: {
  arm1: {arm_name: "text",                   prompt_text, images: []}
  arm2: {arm_name: "multiple images",        prompt_text, images: [6 faces + 2 renders per piece]}
  arm3: {arm_name: "text + multiple images", prompt_text, images: [same as arm2]}
  arm4: {arm_name: "single image",           prompt_text, images: [merged sheet]}
}
```

`prompt_text` is byte-identical to what was sent (`prompt_sha` is included for
verification). Images are sent in the listed order; paths are relative to
`benchmark/`. The held-out face image is the `PREDICT THIS` placeholder, never the
real face — this folder contains no answer-revealing images.

## golden.jsonl

| field | |
|---|---|
| `structure_3d` | the real internal structure, an n×n×n array indexed **`[z][y][x]`**, z = 0 at the bottom. Each cell is the letter of the piece occupying it, or `"."` for empty. |
| `pieces` | the same structure per piece: `{letter: [[x, y, z], ...]}` in block coordinates |
| `held_out` | which face is withheld (`+X -X +Y -Y +Z -Z`); the camera sits on that side and looks inward |
| `answer_grid` | the withheld face: list of n strings, top row first, leftmost character first. Letter = first piece the ray meets, `"."` = see-through. |
| `expected_output` | the output we expect from the model, i.e. the JSON object the prompt asks for. The prompt also asks for a free-text `"reason"` key, which is recorded but not scored. Scoring is an exact match on `answer`. |
| `majority_baseline`, `opposite_baseline` | cell accuracy from always guessing the most common letter, and from mirroring the opposite face |

Screen axes of each face (right, up): `+X`(+Y,+Z) `-X`(-Y,+Z) `+Y`(-X,+Z)
`-Y`(+X,+Z) `+Z`(+X,+Y) `-Z`(-X,+Y). Ray-casting `structure_3d` from `held_out`
with these axes reproduces `answer_grid` exactly. This was checked on all 604 rows.
