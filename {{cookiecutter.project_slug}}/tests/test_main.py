# Copyright Contributors to the {{ cookiecutter.project_name }} project.
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests for the CLI entry point."""

import pytest

from {{ cookiecutter.project_slug }}.main import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]):
    """The entry point runs and prints a greeting."""
    main()
    captured = capsys.readouterr()
    assert "{{ cookiecutter.project_name }}" in captured.out
