# Contributing to SixthView Benchmark

We welcome bug reports, documentation improvements, and benchmark corrections.
All participants must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Issues

Search existing GitHub issues before opening a new issue. For a dataset problem,
include the example ID, affected input arm or image path, expected behavior,
and steps to reproduce it. Use public information in issues and pull requests.

For security vulnerabilities, use [Meta's Bug Bounty program](https://bugbounty.meta.com/)
rather than posting sensitive details in a public issue.

## Pull requests

1. Fork this repository and create a branch from `main`.
2. Make a focused change and update relevant documentation.
3. Run the benchmark validation with Python 3.10 or newer:

   ```bash
   python scripts/check_benchmark.py
   ```

4. For documentation-site changes, use Node.js 22 or newer:

   ```bash
   cd website
   npm ci
   npm run build
   ```

5. Open a pull request explaining the change and how it was checked. Keep
   commit messages short and omit internal project information.
6. Complete the Contributor License Agreement if you have not already done so.

Preserve IDs, JSONL schemas, image order, and image paths when correcting
existing examples. A change to the number of examples or images also needs an
update to the documented counts and validation checks. Describe dataset changes
in [CHANGELOG.md](CHANGELOG.md).

## Contributor License Agreement

Before we can accept your pull request, you must submit a Contributor License
Agreement (CLA). This is required only once for Meta open source projects.
Complete it at https://code.facebook.com/cla.

## License

By contributing, you agree that your contributions will be licensed under the
CC BY-NC 4.0 license in [LICENSE](LICENSE).
