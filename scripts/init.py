# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Initialize a new project from the python-package-template.

This script renames the package directory, updates all references,
resets the version and changelog, and regenerates the lockfile.

Usage:
    uv run --script scripts/init.py
    uv run --script scripts/init.py -- --name my-cool-package
    uv run --script scripts/init.py -- --name my-pkg --author "Jane Smith" \
        --email jane@example.com --github-owner janesmith \
        --description "My awesome package"
    uv run --script scripts/init.py -- --name my-pkg --pypi
    uv run --script scripts/init.py -- --name my-pkg --license mit

Prerequisites:
    - uv installed (https://docs.astral.sh/uv/getting-started/installation/)
    - Run from the project root directory
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STDLIB_NAMES: frozenset[str] = frozenset(
    {
        'abc',
        'ast',
        'asyncio',
        'base64',
        'collections',
        'contextlib',
        'copy',
        'csv',
        'dataclasses',
        'datetime',
        'decimal',
        'enum',
        'functools',
        'hashlib',
        'http',
        'importlib',
        'inspect',
        'io',
        'itertools',
        'json',
        'logging',
        'math',
        'multiprocessing',
        'operator',
        'os',
        'pathlib',
        'pickle',
        'platform',
        'pprint',
        'queue',
        'random',
        're',
        'secrets',
        'shutil',
        'signal',
        'socket',
        'sqlite3',
        'string',
        'struct',
        'subprocess',
        'sys',
        'test',
        'textwrap',
        'threading',
        'time',
        'tomllib',
        'typing',
        'unittest',
        'uuid',
        'warnings',
        'xml',
        'zipfile',
    }
)

SPDX_MAP: dict[str, str] = {
    'agpl-3.0': 'AGPL-3.0-only',
    'apache-2.0': 'Apache-2.0',
    'bsd-2-clause': 'BSD-2-Clause',
    'bsd-3-clause': 'BSD-3-Clause',
    'bsl-1.0': 'BSL-1.0',
    'cc0-1.0': 'CC0-1.0',
    'epl-2.0': 'EPL-2.0',
    'gpl-2.0': 'GPL-2.0-only',
    'gpl-3.0': 'GPL-3.0-only',
    'lgpl-2.1': 'LGPL-2.1-only',
    'mit': 'MIT',
    'mpl-2.0': 'MPL-2.0',
    'unlicense': 'Unlicense',
}

CLASSIFIER_MAP: dict[str, str] = {
    'MIT': 'License :: OSI Approved :: MIT License',
    'Apache-2.0': 'License :: OSI Approved :: Apache Software License',
    'BSD-2-Clause': 'License :: OSI Approved :: BSD License',
    'BSD-3-Clause': 'License :: OSI Approved :: BSD License',
    'GPL-2.0-only': (
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
    ),
    'GPL-3.0-only': (
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ),
    'LGPL-2.1-only': (
        'License :: OSI Approved '
        ':: GNU Lesser General Public License v2 or later (LGPLv2+)'
    ),
    'AGPL-3.0-only': (
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ),
    'MPL-2.0': (
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)'
    ),
    'Unlicense': ('License :: OSI Approved :: The Unlicense (Unlicense)'),
    'BSL-1.0': (
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)'
    ),
    'CC0-1.0': (
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ),
    'EPL-2.0': (
        'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)'
    ),
}


@dataclass(frozen=True)
class LicenseInfo:
    """Metadata for a single license option."""

    key: str
    name: str
    spdx_id: str


OFFLINE_LICENSES: tuple[LicenseInfo, ...] = (
    LicenseInfo('apache-2.0', 'Apache License 2.0', 'Apache-2.0'),
    LicenseInfo('mit', 'MIT License', 'MIT'),
    LicenseInfo(
        'bsd-3-clause',
        'BSD 3-Clause "New" or "Revised" License',
        'BSD-3-Clause',
    ),
    LicenseInfo(
        'gpl-3.0',
        'GNU General Public License v3.0',
        'GPL-3.0-only',
    ),
    LicenseInfo('mpl-2.0', 'Mozilla Public License 2.0', 'MPL-2.0'),
    LicenseInfo('unlicense', 'The Unlicense', 'Unlicense'),
)


# ---------------------------------------------------------------------------
# Name transforms
# ---------------------------------------------------------------------------


def to_snake(name: str) -> str:
    """Convert a package name to snake_case.

    Args:
        name: Package name (may contain hyphens or underscores).

    Returns:
        Name with hyphens replaced by underscores.
    """
    return name.replace('-', '_')


def to_kebab(name: str) -> str:
    """Convert a package name to kebab-case.

    Args:
        name: Package name (may contain hyphens or underscores).

    Returns:
        Name with underscores replaced by hyphens.
    """
    return name.replace('_', '-')


def to_title(name: str) -> str:
    """Convert a package name to Title Case.

    Args:
        name: Package name (may contain hyphens or underscores).

    Returns:
        Title-cased name with separators replaced by spaces.
    """
    return name.replace('-', ' ').replace('_', ' ').title()


# ---------------------------------------------------------------------------
# String escaping
# ---------------------------------------------------------------------------


def escape_toml_string(value: str) -> str:
    """Escape a string for use inside a TOML double-quoted value.

    Backslashes are doubled first, then double quotes are escaped.

    Args:
        value: Raw string to escape.

    Returns:
        TOML-safe escaped string.
    """
    value = value.replace('\\', '\\\\')
    return value.replace('"', '\\"')


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

_NAME_RE = re.compile(r'^[a-z][a-z0-9_-]*$')
_GITHUB_OWNER_RE = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$')


def validate_name(name: str) -> None:
    """Validate a Python package name.

    Args:
        name: Package name to validate.

    Raises:
        ValueError: If the name is invalid.
    """
    if not _NAME_RE.match(name):
        msg = (
            f"Invalid package name: '{name}'. "
            'Must start with a lowercase letter '
            'and contain only [a-z0-9_-].'
        )
        raise ValueError(msg)

    if name in ('python-package-template', 'python_package_template'):
        msg = 'Please choose a name other than the template default.'
        raise ValueError(msg)

    snake = to_snake(name)
    if snake in STDLIB_NAMES:
        msg = (
            f"Package name '{name}' would shadow "
            f"the Python stdlib module '{snake}'."
        )
        raise ValueError(msg)


def validate_email(email: str) -> None:
    """Validate an email address (basic check).

    Args:
        email: Email address to validate.

    Raises:
        ValueError: If the email is invalid.
    """
    if '@' not in email:
        msg = f"Invalid email: '{email}' (must contain @)"
        raise ValueError(msg)
    if '\n' in email or '\r' in email:
        msg = 'Email must be a single line.'
        raise ValueError(msg)


def validate_github_owner(owner: str) -> None:
    """Validate a GitHub username or organization name.

    Args:
        owner: GitHub username or org name.

    Raises:
        ValueError: If the owner name is invalid.
    """
    if not _GITHUB_OWNER_RE.match(owner):
        msg = (
            f"Invalid GitHub owner: '{owner}'. "
            'Must contain only alphanumeric characters or hyphens, '
            'and cannot begin or end with a hyphen.'
        )
        raise ValueError(msg)


def validate_author_name(name: str) -> None:
    """Validate an author name.

    Args:
        name: Author name to validate.

    Raises:
        ValueError: If the author name is invalid.
    """
    if '\n' in name or '\r' in name:
        msg = 'Author name must be a single line.'
        raise ValueError(msg)


def validate_description(description: str) -> None:
    """Validate a project description.

    Args:
        description: Project description to validate.

    Raises:
        ValueError: If the description is empty or multiline.
    """
    if not description.strip():
        msg = 'Description cannot be empty.'
        raise ValueError(msg)
    if '\n' in description or '\r' in description:
        msg = 'Description must be a single line.'
        raise ValueError(msg)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------


def spdx_id_for_key(license_key: str) -> str:
    """Map a GitHub license API key to an SPDX identifier.

    Args:
        license_key: Lowercase license key (e.g. 'mit', 'gpl-3.0').

    Returns:
        SPDX identifier string (e.g. 'MIT', 'GPL-3.0-only').
    """
    return SPDX_MAP.get(license_key, license_key.upper())


def classifier_for_spdx(spdx_id: str) -> str | None:
    """Map an SPDX identifier to a PyPI trove classifier.

    Args:
        spdx_id: SPDX license identifier (e.g. 'MIT').

    Returns:
        Trove classifier string, or None if no mapping exists.
    """
    return CLASSIFIER_MAP.get(spdx_id)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProjectConfig:
    """Immutable container for all project configuration values."""

    name: str
    author: str
    email: str
    github_owner: str
    description: str
    license_key: str
    enable_pypi: bool

    snake_name: str = field(init=False)
    kebab_name: str = field(init=False)
    title_name: str = field(init=False)
    github_repo: str = field(init=False)

    def __post_init__(self) -> None:
        """Compute derived fields from the package name."""
        object.__setattr__(self, 'snake_name', to_snake(self.name))
        object.__setattr__(self, 'kebab_name', to_kebab(self.name))
        object.__setattr__(self, 'title_name', to_title(self.name))
        object.__setattr__(
            self,
            'github_repo',
            f'{self.github_owner}/{to_kebab(self.name)}',
        )
