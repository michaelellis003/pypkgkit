# Copyright Contributors to the pypkgkit project.
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests for the CLI entry point."""

import pytest

from pypkgkit.main import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]):
    """The entry point runs and prints a greeting."""
    main()
    captured = capsys.readouterr()
    assert "pypkgkit" in captured.out
