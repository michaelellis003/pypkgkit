"""Unit tests for the python_package_template module."""

from python_package_template import add, hello, multiply, subtract


def test_hello():
    """Test the hello function."""
    assert hello('World!') == 'Hello World!'


def test_add():
    """Test the add function."""
    assert add(1, 2) == 3


def test_multiply():
    """Test the multiply function."""
    assert multiply(2.5, 2) == 5


def test_subtract_two_positive_integers_returns_difference():
    """Test that subtract returns the difference of two positive integers."""
    assert subtract(5, 3) == 2


def test_subtract_equal_integers_returns_zero():
    """Test that subtract returns zero when both integers are equal."""
    assert subtract(3, 3) == 0


def test_subtract_larger_subtrahend_returns_negative():
    """Test that subtract returns a negative value when b > a."""
    assert subtract(1, 5) == -4
