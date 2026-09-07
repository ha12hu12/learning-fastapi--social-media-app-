import pytest
from app.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 5, 7),
    (6, 5, 11),
    (25, 4, 29)
    ]
)
def test_add(num1, num2, expected):
    print(num1, num2, expected)
    assert add(num1, num2) == expected 

def test_subtract():
    assert subtract(7, 3) == 4 

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(10, 2) == 5

#144. Combining Fixtures + Parametrize 14:55:40

