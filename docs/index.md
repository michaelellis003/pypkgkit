# pypkgkit

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for
Python packages. One command gives you a fully configured project with
linting, type checking, testing, CI/CD, documentation, and automated
releases — all wired together and ready to go.

## Quick start

```bash
uv tool install cookiecutter
cookiecutter gh:michaelellis003/pypkgkit
```

To pin a specific template version, pass the `--checkout` flag with a
release tag:

```bash
cookiecutter gh:michaelellis003/pypkgkit --checkout v2.1.2
```

After answering a few prompts, the template generates a project with
dependencies installed, pre-commit hooks configured, and an initial
commit ready to push.

## Tooling overview

**Package management** is handled by [uv](https://docs.astral.sh/uv/),
which provides fast dependency resolution and a lockfile.

**Code quality** is enforced by [Ruff](https://docs.astral.sh/ruff/)
(linting and formatting) and [ty](https://github.com/astral-sh/ty)
(type checking). Both run as pre-commit hooks and in CI. Every Python
source file carries an
[SPDX license header](https://spdx.dev/learn/handling-license-info/),
enforced by a pre-commit hook and checked in CI.

**Testing** uses [pytest](https://docs.pytest.org/), with CI runs
across Python 3.10 through 3.13 on Linux, macOS, and Windows.

**Documentation** is built with
[ProperDocs](https://properdocs.dev/)
([MkDocs Material](https://squidfunk.github.io/mkdocs-material/) +
[mkdocstrings](https://mkdocstrings.github.io/)), which generates API
reference pages directly from docstrings in the source.

**Versioning** follows
[Conventional Commits](https://www.conventionalcommits.org/).
[python-semantic-release](https://python-semantic-release.readthedocs.io/)
reads the commit history on each push to `main` and determines whether
a new version should be published. If so, it bumps the version, tags
the commit, creates a GitHub release, generates the changelog, and
publishes to PyPI — all without manual intervention.

**Dependency updates** are handled by
[Dependabot](https://docs.github.com/en/code-security/dependabot),
configured to open PRs weekly for both GitHub Actions and pip
dependencies.

**Typing** follows [PEP 561](https://peps.python.org/pep-0561/). The
generated package ships a `py.typed` marker, so downstream consumers
get full type information.

## Template variables

| Variable | Default | Description |
|---|---|---|
| `project_name` | `my-python-package` | Name of the project |
| `project_slug` | *auto* | Python-importable name |
| `project_description` | `A Python package` | One-line description |
| `author_name` | `Your Name` | Author name |
| `author_email` | `you@example.com` | Author email |
| `github_username` | `your-github-username` | GitHub username |
| `python_version` | `3.12` | Minimum Python version |
| `initial_version` | `0.1.0` | Starting version |

## Generated project structure

```
my_python_package/
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── actions/setup-uv/action.yml
│   └── workflows/
│       ├── ci.yml
│       ├── dependabot-automerge.yml
│       ├── docs.yml
│       └── release.yml
├── docs/
│   ├── api.md
│   ├── gen_ref_pages.py
│   └── index.md
├── scripts/
│   └── update_headers.py
├── src/my_python_package/
│   ├── __init__.py
│   ├── main.py
│   └── py.typed
├── tests/
│   ├── __init__.py
│   └── test_version.py
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── LICENSE
├── Makefile
├── README.md
├── mkdocs.yml
├── pyproject.toml
└── uv.lock
```

## Makefile

Each generated project includes a `Makefile` with common tasks:

| Target | What it does |
|---|---|
| `make test` | Lint, then run pytest |
| `make lint` | Ruff check, format check, license header check, ty |
| `make format` | Add license headers, ruff format, ruff fix |
| `make license` | Add missing SPDX license headers |
| `make docs` | Build documentation |
| `make serve-docs` | Serve documentation locally |
| `make install` | `uv sync` |
| `make clean` | `git clean` (preserves `.venv`) |

## CI/CD pipeline

The pipeline is split into three GitHub Actions workflows, each gated
on the success of the previous one:

1. **CI** — runs on every push and pull request to `main`. Checks
   linting, formatting, type correctness, tests (across four Python
   versions and three operating systems), code coverage, lockfile
   integrity, and package build validity.

2. **Release** — triggered after CI succeeds on `main`. Runs
   `python-semantic-release` to determine if a new version is needed.
   If so, bumps the version, generates the changelog, and publishes
   the package to PyPI using trusted publishing.

3. **Docs** — triggered after Release succeeds. Deploys the
   documentation to GitHub Pages.

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

## License

Apache 2.0. See [LICENSE](https://github.com/michaelellis003/pypkgkit/blob/main/LICENSE)
for the full text.
