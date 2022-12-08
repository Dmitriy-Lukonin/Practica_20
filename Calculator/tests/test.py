
# 1. PyCharm —> Preferences —> Tools —> Python integration tools и в разделе Testing выбираем PyTest.

import pytest

from app.calc import Calculator

# def test_sum():
#     assert 2 + 2 == 4

# ============================= test session starts =============================
# collecting ... collected 1 item
#
# test.py::test_sum PASSED                                                 [100%]
#
# ============================== 1 passed in 0.02s ==============================


class TestCalc:
    def setup(self):
        self.calc = Calculator()

    def test_multiply_succes(self):
        assert self.calc.multiply(5, 5) == 25

    def test_division_succes(self):
        assert self.calc.division(10, 5) == 2

    def test_subtraction_success(self):
        assert self.calc.subtraction(5, 1) == 4

    def test_adding_succes(self):
        assert self.calc.adding(2, 2) == 4

    def test_multiply_unsuccess(self):
        assert self.calc.multiply(5, 5) == 10

    def test_division_unsucces(self):
        assert self.calc.division(10, 5) == 1

    def test_subtraction_unsuccess(self):
        assert self.calc.subtraction(5, 1) == 5

    def test_adding_unsuccess(self):
        assert self.calc.adding(2, 2) == 5



    def test_zero_division(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(1, 0)

    def teardown(self):
        print('Выполнение метода Teardown')
