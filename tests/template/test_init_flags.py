"""Tests for init.sh flag validation and special character handling.

These tests verify that init.sh properly validates flag arguments
and handles special characters in user-provided values.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

# Directories to exclude when copying the repo to a tmpdir
_EXCLUDE_DIRS = {
    '.git',
    '.venv',
    '.ruff_cache',
    '.pytest_cache',
    '__pycache__',
    'node_modules',
}


def _ignore_dirs(directory: str, contents: list[str]) -> set[str]:
    """Return set of directory names to exclude from shutil.copytree."""
    return {c for c in contents if c in _EXCLUDE_DIRS}


@pytest.mark.integration
@pytest.mark.slow
def test_init_flag_without_value_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.sh exits with error when flag has no value."""
    project = tmp_path / 'project'
    shutil.copytree(template_dir, project, ignore=_ignore_dirs)

    init_script = project / 'scripts' / 'init.sh'
    init_script.chmod(0o755)

    result = subprocess.run(
        [str(init_script), '--name'],
        cwd=str(project),
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'requires a value' in result.stderr, (
        f'Expected "requires a value" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_description_with_pipe_preserved_in_pyproject(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that description with pipe character is preserved."""
    project = tmp_path / 'project'
    shutil.copytree(template_dir, project, ignore=_ignore_dirs)

    init_script = project / 'scripts' / 'init.sh'
    init_script.chmod(0o755)

    description = 'CLI tools | Python utilities'

    result = subprocess.run(
        [
            str(init_script),
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'testowner',
            '--description',
            description,
            '--license',
            'mit',
        ],
        cwd=str(project),
        input='n\ny\n',
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, (
        f'init.sh failed (rc={result.returncode})\n'
        f'STDOUT:\n{result.stdout}\n'
        f'STDERR:\n{result.stderr}'
    )

    pyproject = (project / 'pyproject.toml').read_text()
    assert description in pyproject, (
        f'Description not found in pyproject.toml.\n'
        f'Expected: {description}\n'
        f'pyproject.toml content:\n{pyproject}'
    )
