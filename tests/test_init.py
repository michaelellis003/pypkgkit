from python_package_template import add, hello, multiply, subtract


def test_hello_with_custom_name_returns_greeting():
    assert hello('World!') == 'Hello World!'


def test_hello_default_name_returns_hello_world():
    assert hello() == 'Hello world'


def test_hello_with_empty_string_returns_hello():
    assert hello('') == 'Hello '


def test_add_two_positive_integers_returns_sum():
    assert add(1, 2) == 3


def test_add_with_zero_returns_same_number():
    assert add(5, 0) == 5


def test_add_negative_numbers_returns_sum():
    assert add(-3, -7) == -10


def test_subtract_two_positive_integers_returns_difference():
    assert subtract(5, 3) == 2


def test_subtract_equal_integers_returns_zero():
    assert subtract(3, 3) == 0


def test_subtract_larger_subtrahend_returns_negative():
    assert subtract(1, 5) == -4


def test_multiply_float_by_integer_returns_product():
    assert multiply(2.5, 2) == 5.0


def test_multiply_by_zero_returns_zero():
    assert multiply(3.14, 0) == 0.0


def test_multiply_negative_float_returns_correct_product():
    assert multiply(-2.5, 3) == -7.5
