# pypkgkit

[![CI](https://github.com/michaelellis003/pypkgkit/actions/workflows/ci.yml/badge.svg)](https://github.com/michaelellis003/pypkgkit/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pypkgkit)](https://pypi.org/project/pypkgkit/)
[![License](https://img.shields.io/github/license/michaelellis003/pypkgkit)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://michaelellis003.github.io/pypkgkit/)

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for
Python packages. One command gives you a fully configured project with
linting, type checking, testing, CI/CD, documentation, and automated
releases — all wired together and ready to go.

## Quick start

```bash
# Install cookiecutter if you haven't already
uv tool install cookiecutter

# Generate a new project
cookiecutter gh:michaelellis003/pypkgkit
```

You will be prompted for a few values:

| Variable | Default | Description |
|---|---|---|
| `project_name` | `my-python-package` | Name of the project (used in PyPI, GitHub, etc.) |
| `project_slug` | *auto* | Python-importable name (derived from project name) |
| `project_description` | `A Python package` | One-line description |
| `author_name` | `Your Name` | Author name for pyproject.toml and LICENSE |
| `author_email` | `you@example.com` | Author email |
| `github_username` | `your-github-username` | GitHub username (used in URLs, badges, CODEOWNERS) |
| `python_version` | `3.12` | Minimum Python version |
| `initial_version` | `0.1.0` | Starting version |

After generation, the template automatically:

1. Initializes a git repository
2. Installs dependencies with `uv sync`
3. Installs pre-commit hooks
4. Creates an initial commit

## What is included

Every generated project comes with:

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

## After generating your project

1. Create a GitHub repo and push:

   ```bash
   git remote add origin https://github.com/<username>/<project-name>.git
   git push -u origin main
   ```

2. Configure GitHub settings:
   - **GitHub Pages**: Settings > Pages > Source: `gh-pages`
   - **RELEASE_TOKEN**: Settings > Secrets — a PAT with `contents: write`
   - **PyPI trusted publishing**: add the repo on pypi.org
   - **CODECOV_TOKEN**: Settings > Secrets (optional)

## Requirements

- [uv](https://docs.astral.sh/uv/) installed
- [cookiecutter](https://cookiecutter.readthedocs.io/) (`uv tool install cookiecutter`)

## Contributing

To work on the template itself:

```bash
git clone https://github.com/michaelellis003/pypkgkit.git
cd pypkgkit
uv sync
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install --hook-type pre-push
```

Test the template locally:

```bash
cookiecutter . --no-input
```

## License

Apache 2.0. See [LICENSE](LICENSE) for the full text.
