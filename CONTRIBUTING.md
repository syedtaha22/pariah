# Contributing

## Setup

Install [uv](https://docs.astral.sh/uv/), then from the repository root:

```bash
uv sync            # create .venv from pyproject.toml and uv.lock
uv run pytest      # run the tests
uv run ruff check  # lint
```

Dependencies should be changed with `uv add` or `uv remove`, so `uv.lock` stays in sync and is
committed together with `pyproject.toml`.

## Branching

- `main` should always be in a working state: tests and lint pass, and the environment installs.
- Nobody should push directly to `main`. Every change should go through a pull request.
- Work should happen on short-lived branches created from an up-to-date `main`.
- Branch names should follow `<type>/<short-description>` in lowercase with hyphens, where
  `<type>` is one of:

  | Type | Use |
  | --- | --- |
  | `feat` | new functionality |
  | `fix` | bug fix |
  | `exp` | experiment code or configs |
  | `data` | dataset loading, cleaning or generators |
  | `docs` | documentation only |
  | `refactor` | restructuring without behavior change |
  | `test` | tests only |
  | `chore` | tooling, dependencies, housekeeping |

  For example: `feat/graphgps-encoder`, `fix/seed-cuda-determinism`.
- A branch should be deleted after it is merged.

## Commits

- Commit messages should follow [Conventional Commits](https://www.conventionalcommits.org/):
  `<type>: <summary>`, using the same types as branches (`feat`, `fix`, `exp`, `data`, `docs`,
  `refactor`, `test`, `chore`).
- The summary should be in the imperative mood, start lowercase, have no trailing period and stay
  within 72 characters. For example: `feat: add group dro loss`.
- The body, when present, should be separated by a blank line and explain why the change is made,
  not only what changed.
- Each commit should be one logical change and should leave tests and lint passing.
- Generated or large files should not be committed: datasets, checkpoints, run outputs and virtual
  environments are covered by `.gitignore`.

## Pull requests

- A pull request should target `main`, stay focused on one change, and fill in the pull request
  template.
- It should be reviewed and approved by at least one author other than its creator before merging.
- All review comments should be resolved before merging.
- Merging should use squash, so `main` keeps one commit per pull request. The squash commit message
  should follow the commit format above.
- Related issues should be linked with `Closes #<number>`.

## Coding standards

- Python 3.12. Formatting and linting are handled by ruff with the settings in `pyproject.toml`
  (line length 100). `uv run ruff check` should report no errors before a commit.
- Code should follow PEP 8 naming: `snake_case` for functions, variables and modules,
  `PascalCase` for classes, `UPPER_CASE` for constants.
- Function signatures should have type hints, and public functions, classes and modules should
  have docstrings.
- Comments should explain why something is done, not restate what the code does.
- Modules should be imported through the `src` package (`from src.utils.seed import seed_everything`),
  not through path manipulation.
- Values that change between experiments (learning rate, model, dataset, seed) should live in YAML
  configs under `configs/`, not in code.
- Randomness should be seeded with `seed_everything` from `src/utils/seed.py`. Results should be
  logged with `CSVLogger` from `src/utils/logger.py`, together with the config hash from
  `src/utils/config.py` and the seed.
- Paths should be built with `pathlib` and be relative to the repository, not absolute.
- New behavior should come with tests under `tests/`, mirroring the layout of `src/`. Tests should
  be deterministic and fast, and should not download data.
- Notebooks, if used, should be committed with outputs cleared.
