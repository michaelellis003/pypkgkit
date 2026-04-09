# pypkgkit

A minimal, opinionated template for Python packages.

## Motivation

Starting a new Python project involves a surprisingly large number of
decisions that have nothing to do with the project itself: which
linter, which formatter, how to structure CI, how to automate releases,
how to generate documentation. These choices are largely orthogonal to
the actual work, yet getting them wrong — or deferring them — tends to
create friction later.

pypkgkit assembles a reasonable set of modern tools into a single
template so that new projects inherit a working development
environment from the outset.

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
package ships a `py.typed` marker, so downstream consumers get full
type information when importing from pypkgkit.

## Quick start

```bash
git clone https://github.com/michaelellis003/pypkgkit.git
cd pypkgkit
uv sync
```

Install the pre-commit hooks (this only needs to be done once):

```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install --hook-type pre-push
```

## Makefile

A `Makefile` collects the common development commands:

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

## Conventional Commits

All commit messages must follow the
[Conventional Commits](https://www.conventionalcommits.org/) spec. A
pre-commit hook enforces this at commit time. The format is:

```
<type>: <description>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`,
`ci`. Only `feat` and `fix` (and breaking changes) trigger version
bumps; the others are recorded in the history but do not produce a
release.

## License

Apache 2.0. See [LICENSE](https://github.com/michaelellis003/pypkgkit/blob/main/LICENSE)
for the full text.
