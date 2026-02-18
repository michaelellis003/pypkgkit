"""Tests for init.py flag validation and special character handling.

These tests verify that init.py properly validates flag arguments
and handles special characters in user-provided values.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

# Directories/files to exclude when copying the repo to a tmpdir
_EXCLUDE_DIRS = {
    '.git',
    '.venv',
    '.ruff_cache',
    '.pytest_cache',
    '__pycache__',
    'node_modules',
    'site',
    'dist',
    'build',
    '.coverage',
}

# Standard flags that provide all required inputs for init.py
_ALL_FLAGS = [
    '--name',
    'test-pkg',
    '--author',
    'Test Author',
    '--email',
    'test@example.com',
    '--github-owner',
    'testowner',
    '--description',
    'A test package',
    '--license',
    'mit',
]


def _ignore_dirs(directory: str, contents: list[str]) -> set[str]:
    """Return set of directory names to exclude from shutil.copytree."""
    return {c for c in contents if c in _EXCLUDE_DIRS}


def _setup_project(tmp_path, template_dir):
    """Copy template to tmpdir and return (project_path, init_script)."""
    project = tmp_path / 'project'
    shutil.copytree(template_dir, project, ignore=_ignore_dirs)
    init_script = project / 'scripts' / 'init.py'
    return project, init_script


def _run_init(init_script, project, extra_args=None, stdin_text=''):
    """Run init.py via uv and return the CompletedProcess."""
    cmd = ['uv', 'run', '--script', str(init_script)]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(
        cmd,
        cwd=str(project),
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_flag_without_value_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.py exits with error when flag has no value."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(init_script, project, extra_args=['--name'])

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'expected one argument' in result.stderr, (
        f'Expected "expected one argument" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_description_with_pipe_preserved_in_pyproject(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that description with pipe character is preserved."""
    project, init_script = _setup_project(tmp_path, template_dir)

    description = 'CLI tools | Python utilities'

    result = _run_init(
        init_script,
        project,
        extra_args=[
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
        stdin_text='y\n',
    )

    assert result.returncode == 0, (
        f'init.py failed (rc={result.returncode})\n'
        f'STDOUT:\n{result.stdout}\n'
        f'STDERR:\n{result.stderr}'
    )

    pyproject = (project / 'pyproject.toml').read_text()
    assert description in pyproject, (
        f'Description not found in pyproject.toml.\n'
        f'Expected: {description}\n'
        f'pyproject.toml content:\n{pyproject}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_stdlib_name_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.py rejects names that shadow stdlib modules."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=['--name', 'json'],
    )

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'shadow' in result.stderr, (
        f'Expected "shadow" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_invalid_github_owner_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.py rejects invalid GitHub owner names."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=[
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'My Awesome Org!',
            '--description',
            'A test package',
            '--license',
            'mit',
        ],
        stdin_text='y\n',
    )

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'Invalid GitHub owner' in result.stderr, (
        f'Expected "Invalid GitHub owner" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_missing_required_field_noninteractive_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.py errors when required input is missing."""
    project, init_script = _setup_project(tmp_path, template_dir)

    # Provide --name but omit --author; stdin is a pipe (non-interactive)
    result = _run_init(
        init_script,
        project,
        extra_args=['--name', 'test-pkg'],
    )

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'required' in result.stderr, (
        f'Expected "required" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_description_whitespace_trimmed(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that leading/trailing whitespace is trimmed."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=[
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'testowner',
            '--description',
            '  My awesome package  ',
            '--license',
            'none',
        ],
        stdin_text='y\n',
    )

    assert result.returncode == 0, (
        f'init.py failed (rc={result.returncode})\n'
        f'STDOUT:\n{result.stdout}\n'
        f'STDERR:\n{result.stderr}'
    )

    pyproject = (project / 'pyproject.toml').read_text()
    assert 'My awesome package' in pyproject
    # Verify leading/trailing spaces were stripped
    assert '  My awesome package  ' not in pyproject


@pytest.mark.integration
@pytest.mark.slow
def test_init_description_with_double_quotes_produces_valid_toml(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that description with double quotes is TOML-escaped."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=[
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'testowner',
            '--description',
            'A toolkit for "smart" parsing',
            '--license',
            'mit',
        ],
        stdin_text='y\n',
    )

    assert result.returncode == 0, (
        f'init.py failed (rc={result.returncode})\n'
        f'STDOUT:\n{result.stdout}\n'
        f'STDERR:\n{result.stderr}'
    )

    pyproject = (project / 'pyproject.toml').read_text()
    assert r'\"smart\"' in pyproject, (
        f'Expected escaped quotes in pyproject.toml.\n'
        f'pyproject.toml content:\n{pyproject}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_empty_description_noninteractive_exits_with_error(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that init.py rejects empty description in non-interactive."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=[
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'testowner',
            '--description',
            '',
            '--license',
            'none',
        ],
    )

    assert result.returncode != 0, (
        f'Expected non-zero exit code, got {result.returncode}'
    )
    assert 'required' in result.stderr, (
        f'Expected "required" in stderr, got: {result.stderr}'
    )


@pytest.mark.integration
@pytest.mark.slow
def test_init_description_with_backslash_produces_valid_toml(
    tmp_path: Path,
    template_dir: Path,
):
    """Test that description with backslash is TOML-escaped."""
    project, init_script = _setup_project(tmp_path, template_dir)

    result = _run_init(
        init_script,
        project,
        extra_args=[
            '--name',
            'test-pkg',
            '--author',
            'Test Author',
            '--email',
            'test@example.com',
            '--github-owner',
            'testowner',
            '--description',
            'Supports C:\\new stuff',
            '--license',
            'mit',
        ],
        stdin_text='y\n',
    )

    assert result.returncode == 0, (
        f'init.py failed (rc={result.returncode})\n'
        f'STDOUT:\n{result.stdout}\n'
        f'STDERR:\n{result.stderr}'
    )

    pyproject = (project / 'pyproject.toml').read_text()
    assert 'C:\\\\new' in pyproject, (
        f'Expected escaped backslash in pyproject.toml.\n'
        f'pyproject.toml content:\n{pyproject}'
    )
