"""Tests for pypkgkit.defaults module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from pypkgkit.defaults import (
    derive_package_name,
    detect_gh_owner,
    detect_git_user_email,
    detect_git_user_name,
)


class TestDetectGitUserName:
    def test_returns_name_on_success(self):
        mock_result = MagicMock(returncode=0, stdout='Jane Smith\n')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_git_user_name() == 'Jane Smith'

    def test_returns_none_on_failure(self):
        mock_result = MagicMock(returncode=1, stdout='')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_git_user_name() is None

    def test_returns_none_on_empty_output(self):
        mock_result = MagicMock(returncode=0, stdout='  \n')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_git_user_name() is None

    def test_returns_none_on_file_not_found(self):
        with patch(
            'pypkgkit.defaults.subprocess.run',
            side_effect=FileNotFoundError,
        ):
            assert detect_git_user_name() is None


class TestDetectGitUserEmail:
    def test_returns_email_on_success(self):
        mock_result = MagicMock(returncode=0, stdout='jane@example.com\n')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_git_user_email() == 'jane@example.com'

    def test_returns_none_on_failure(self):
        mock_result = MagicMock(returncode=1, stdout='')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_git_user_email() is None

    def test_returns_none_on_file_not_found(self):
        with patch(
            'pypkgkit.defaults.subprocess.run',
            side_effect=FileNotFoundError,
        ):
            assert detect_git_user_email() is None


class TestDetectGhOwner:
    def test_returns_login_on_success(self):
        mock_result = MagicMock(returncode=0, stdout='janesmith\n')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_gh_owner() == 'janesmith'

    def test_returns_none_on_failure(self):
        mock_result = MagicMock(returncode=1, stdout='')
        with patch(
            'pypkgkit.defaults.subprocess.run',
            return_value=mock_result,
        ):
            assert detect_gh_owner() is None

    def test_returns_none_on_file_not_found(self):
        with patch(
            'pypkgkit.defaults.subprocess.run',
            side_effect=FileNotFoundError,
        ):
            assert detect_gh_owner() is None


class TestDerivePackageName:
    def test_returns_kebab_from_directory_name(self):
        assert derive_package_name('my-cool-project') == 'my-cool-project'

    def test_converts_underscores_to_hyphens(self):
        assert derive_package_name('my_cool_project') == 'my-cool-project'

    def test_returns_none_for_empty_string(self):
        assert derive_package_name('') is None

    def test_lowercases_name(self):
        assert derive_package_name('My-Project') == 'my-project'
