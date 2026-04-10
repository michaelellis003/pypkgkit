# Copyright Contributors to the pypkgkit project.
# SPDX-License-Identifier: Apache-2.0

# !/usr/bin/env python
"""Post-generation hook for the pypkgkit cookiecutter template."""

import datetime
import pathlib
import subprocess


def replace_copyright_year():
    """Replace the copyright year placeholder with the current year."""
    year = str(datetime.datetime.now(tz=datetime.timezone.utc).year)
    license_path = pathlib.Path("LICENSE")
    text = license_path.read_text()
    text = text.replace("COPYRIGHT_YEAR_PLACEHOLDER", year)
    license_path.write_text(text)


def init_git():
    """Initialize a git repository with a main branch."""
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "checkout", "-b", "main"], check=True)


def install_dependencies():
    """Install project dependencies with uv."""
    subprocess.run(["uv", "sync"], check=True)


def install_pre_commit_hooks():
    """Install all pre-commit hook types."""
    subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
    subprocess.run(
        ["uv", "run", "pre-commit", "install", "--hook-type", "commit-msg"],
        check=True,
    )
    subprocess.run(
        ["uv", "run", "pre-commit", "install", "--hook-type", "pre-push"],
        check=True,
    )


def initial_commit():
    """Create the initial commit."""
    import os

    env = {**os.environ, "SKIP": "conventional-pre-commit"}
    msg = "feat: initial project from pypkgkit template"
    subprocess.run(["git", "add", "."], check=True)
    result = subprocess.run(["git", "commit", "-m", msg], env=env)
    if result.returncode != 0:
        # Pre-commit hooks may have auto-fixed files; re-stage and retry.
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", msg], check=True, env=env)


def main():
    """Run all post-generation steps."""
    print("\n--- Setting up your new project ---\n")

    print("Setting copyright year...")
    replace_copyright_year()

    print("Initializing git repository...")
    init_git()

    print("Installing dependencies with uv...")
    install_dependencies()

    print("Installing pre-commit hooks...")
    install_pre_commit_hooks()

    print("Creating initial commit...")
    initial_commit()

    print("\n--- Setup complete! ---")
    print("Your project is ready. Next steps:")
    print(
        "  1. Create a GitHub repo and push:\n"
        "     git remote add origin "
        "https://github.com/{{ cookiecutter.github_username }}/"
        "{{ cookiecutter.project_name }}.git\n"
        "     git push -u origin main"
    )
    print("  2. Enable GitHub Pages (Settings > Pages > Source: gh-pages)")
    print("  3. Add RELEASE_TOKEN secret (Settings > Secrets)")
    print("  4. Set up PyPI trusted publishing")
    print("  5. Add CODECOV_TOKEN secret if using Codecov")


if __name__ == "__main__":
    main()
