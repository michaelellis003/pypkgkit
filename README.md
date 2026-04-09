# pypkgkit

A minimal, opinionated template for Python packages.

The goal is straightforward: provide a single starting point that
assembles modern Python tooling into a coherent whole, so that new
projects begin with CI, documentation, and release automation already
in place — rather than reinventing this infrastructure each time.

## What is included

| Concern | Tool |
|---|---|
| Package management | [uv](https://docs.astral.sh/uv/) |
| Linting & formatting | [Ruff](https://docs.astral.sh/ruff/) |
| Type checking | [ty](https://github.com/astral-sh/ty) |
| Testing | [pytest](https://docs.pytest.org/) |
| Documentation | [ProperDocs](https://properdocs.dev/) ([MkDocs Material](https://squidfunk.github.io/mkdocs-material/) + [mkdocstrings](https://mkdocstrings.github.io/)) |
| Versioning & releases | [python-semantic-release](https://python-semantic-release.readthedocs.io/) with [Conventional Commits](https://www.conventionalcommits.org/) |
| CI/CD | GitHub Actions (lint, type check, test across 3.10 – 3.13, build, release to PyPI, deploy docs) |
| Dependency updates | [Dependabot](https://docs.github.com/en/code-security/dependabot) (weekly, for both Actions and pip) |
| Pre-commit hooks | Ruff, ty, license headers, conventional commit validation |

## Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) installed

## Getting started

Clone the repository and install dependencies:

```bash
git clone https://github.com/michaelellis003/pypkgkit.git
cd pypkgkit
uv sync
```

Install the pre-commit hooks:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install --hook-type pre-push
```

## Development

A `Makefile` is provided for common tasks:

```bash
make test        # lint + pytest
make lint        # ruff check, format check, license headers, ty
make format      # add license headers, ruff format, ruff fix
make license     # add missing license headers
make docs        # build documentation
make serve-docs  # serve documentation locally
make install     # uv sync
make clean       # git clean (preserves .venv)
```

Or invoke tools directly:

```bash
uv run pytest -v
uv run ruff check .
uv run ruff format .
uv run ty check
uv run properdocs serve
```

## How releases work

Releases are fully automated. When a commit lands on `main` and CI
passes, `python-semantic-release` inspects the commit history to
determine whether a version bump is warranted:

- `fix: ...` produces a patch release (0.1.0 &rarr; 0.1.1)
- `feat: ...` produces a minor release (0.1.0 &rarr; 0.2.0)
- A `BREAKING CHANGE` footer or `!` suffix produces a major release (0.1.0 &rarr; 1.0.0)

If a bump is triggered, the pipeline updates the version in
`pyproject.toml` and `src/pypkgkit/__init__.py`, creates a Git tag and
GitHub release, generates the changelog, builds the package, and
publishes it to PyPI via trusted publishing. Documentation is deployed
to GitHub Pages immediately after.

Commit messages that do not follow the
[Conventional Commits](https://www.conventionalcommits.org/) spec are
rejected by a pre-commit hook, so the release process stays
well-defined.

## License

Apache 2.0. See [LICENSE](LICENSE) for the full text.
