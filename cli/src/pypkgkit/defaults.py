"""Smart default detection for interactive prompts."""

from __future__ import annotations

import subprocess


def detect_git_user_name() -> str | None:
    """Detect the user's name from ``git config user.name``.

    Returns:
        User name string, or None on any failure.
    """
    return _run_command('git', 'config', 'user.name')


def detect_git_user_email() -> str | None:
    """Detect the user's email from ``git config user.email``.

    Returns:
        Email string, or None on any failure.
    """
    return _run_command('git', 'config', 'user.email')


def detect_gh_owner() -> str | None:
    """Detect the GitHub username from ``gh api user``.

    Returns:
        GitHub login string, or None on any failure.
    """
    return _run_command('gh', 'api', 'user', '--jq', '.login')


def derive_package_name(directory_name: str) -> str | None:
    """Derive a kebab-case package name from a directory name.

    Args:
        directory_name: The directory name to derive from.

    Returns:
        Kebab-case name, or None if the input is empty.
    """
    name = directory_name.strip().lower().replace('_', '-')
    return name or None


def _run_command(*args: str) -> str | None:
    """Run a command and return stripped stdout, or None on failure.

    Args:
        args: Command and arguments.

    Returns:
        Stripped stdout, or None on any failure.
    """
    try:
        result = subprocess.run(
            list(args),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        value = result.stdout.strip()
        return value or None
    except FileNotFoundError:
        return None
