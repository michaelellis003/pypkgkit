# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }})](https://pypi.org/project/{{ cookiecutter.project_name }}/)
[![License](https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }})](LICENSE)

{{ cookiecutter.project_description }}

## Requirements

- Python {{ cookiecutter.python_version }} or later
- [uv](https://docs.astral.sh/uv/) installed

## Getting started

Clone the repository and install dependencies:

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}.git
cd {{ cookiecutter.project_name }}
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

## How releases work

Releases are fully automated. When a commit lands on `main` and CI
passes, `python-semantic-release` inspects the commit history to
determine whether a version bump is warranted:

- `fix: ...` produces a patch release
- `feat: ...` produces a minor release
- A `BREAKING CHANGE` footer or `!` suffix produces a major release

## License

Apache 2.0. See [LICENSE](LICENSE) for the full text.
