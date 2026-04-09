# Copyright Contributors to the pypkgkit project.
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests for pypkgkit."""

import pypkgkit


def test_version_is_set():
    """The package exposes a version string."""
    assert isinstance(pypkgkit.__version__, str)
    assert len(pypkgkit.__version__) > 0
