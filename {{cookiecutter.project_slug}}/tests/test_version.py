# Copyright Contributors to the {{ cookiecutter.project_name }} project.
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests for {{ cookiecutter.project_name }}."""

import {{ cookiecutter.project_slug }}


def test_version_is_set():
    """The package exposes a version string."""
    assert isinstance({{ cookiecutter.project_slug }}.__version__, str)
    assert len({{ cookiecutter.project_slug }}.__version__) > 0
