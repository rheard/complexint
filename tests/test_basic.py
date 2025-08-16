"""These are simple tests to verify complexint acts very similar to complex, but just with int output"""

from pathlib import Path
from typing import Union

import complexint

from complexint import complexint as complexi

def test_compiled_tests():
    """Verify that we are running these tests with a compiled version of complexint"""
    path = Path(complexint.__file__)
    return path.suffix.lower() == '.pyd'


def test_precision():
    """Test the purpose of this package: the difference in precision when compared to complex"""
    # This number + 1 has too much precision to be stored in a double
    LAST_NUM = 2 ** 53

    a = complex(LAST_NUM, 1)
    b = complex(LAST_NUM, 1)
    c = complexi(LAST_NUM, 1)
    assert a.real == b.real
    assert a.real == c.real

    b += 1  # Add 1 to b theoretically, but because double is limited, not actually changing the value
    assert a.real == b.real

    c += 1  # Add 1 to c actually, getting a different value
    assert b.real != c.real


def test_int_precision():
    """Validate mypyc isn't using limited-precision integers like int64 or something"""
    LAST_NUM = 2 ** 64

    a = complexi(LAST_NUM, 1)
    assert a.real == LAST_NUM

    a += 1
    assert a.real != LAST_NUM
    assert a.real > 100


class ComplexIntTests:
    """Support methods for testing complexint"""
    a, b, a_int, b_int = None, None, None, None

    def setup_method(self, _):
        """Setup some test data"""
        self.a = complex(1, 2)
        self.b = complex(3, 6)

        self.a_int = complexi(1, 2)
        self.b_int = complexi(3, 6)

    @staticmethod
    def assert_complex_equal(res: Union[complex, complexi], res_int: complexi):
        """Validate the complexint is equal to the validation object, and that it is still backed by integers"""
        assert res.real == res_int.real
        assert res.imag == res_int.imag

        assert isinstance(res_int.real, int)
        assert isinstance(res_int.imag, int)


class TestAdd(ComplexIntTests):
    """Tests for __add__"""

    def test_add(self):
        """Test complexint + complexint"""
        res = self.a + self.b
        res_int = self.a_int + self.b_int

        self.assert_complex_equal(res, res_int)

    def test_add_int(self):
        """Test complexint + int"""
        for i in range(100):
            res = self.a + i
            res_int = self.a_int + i

            self.assert_complex_equal(res, res_int)

    def test_add_int_reversed(self):
        """Test int + complexint"""
        for i in range(100):
            res = i + self.a
            res_int = i + self.a_int

            self.assert_complex_equal(res, res_int)

    def test_add_complex(self):
        """Test complexint + complex"""
        res = self.a + (2 + 1j)
        res_int = self.a_int + (2 + 1j)

        self.assert_complex_equal(res, res_int)

    def test_add_complex_reversed(self):
        """Test complex + complexint"""
        res = (2 + 1j) + self.a
        res_int = (2 + 1j) + self.a_int

        self.assert_complex_equal(res, res_int)


class TestSub(ComplexIntTests):
    """Tests for __sub__"""

    def test_sub(self):
        """Test complexint - complexint"""
        res = self.a - self.b
        res_int = self.a_int - self.b_int

        self.assert_complex_equal(res, res_int)

    def test_sub_int(self):
        """Test complexint - int"""
        for i in range(100):
            res = self.a - i
            res_int = self.a_int - i

            self.assert_complex_equal(res, res_int)

    def test_sub_int_reversed(self):
        """Test int - complexint"""
        for i in range(100):
            res = i - self.a
            res_int = i - self.a_int

            self.assert_complex_equal(res, res_int)

    def test_sub_complex(self):
        """Test complexint - complex"""
        res = self.a - (2 + 1j)
        res_int = self.a_int - (2 + 1j)

        self.assert_complex_equal(res, res_int)

    def test_sub_complex_reversed(self):
        """Test complex - complexint"""
        res = (2 + 1j) - self.a
        res_int = (2 + 1j) - self.a_int

        self.assert_complex_equal(res, res_int)


class TestNegPos(ComplexIntTests):
    """Tests for __neg__ and __pos__"""

    def test_neg(self):
        """Test -complexint"""
        res = -self.a
        res_int = -self.a_int

        self.assert_complex_equal(res, res_int)

    def test_pos(self):
        """Test +complexint"""
        res = +self.a
        res_int = +self.a_int

        self.assert_complex_equal(res, res_int)


class TestMul(ComplexIntTests):
    """Tests for __mul__"""

    def test_mul(self):
        """Test complexint * complexint"""
        res = self.a * self.b
        res_int = self.a_int * self.b_int

        self.assert_complex_equal(res, res_int)

    def test_mul_int(self):
        """Test complexint * int"""
        for i in range(100):
            res = self.a * i
            res_int = self.a_int * i

            self.assert_complex_equal(res, res_int)

    def test_mul_int_reversed(self):
        """Test int * complexint"""
        for i in range(100):
            res = i * self.a
            res_int = i * self.a_int

            self.assert_complex_equal(res, res_int)

    def test_mul_complex(self):
        """Test complexint * complex"""
        res = self.a * (2 + 1j)
        res_int = self.a_int * (2 + 1j)

        self.assert_complex_equal(res, res_int)

    def test_mul_complex_reversed(self):
        """Test complex * complexint"""
        res = (2 + 1j) * self.a
        res_int = (2 + 1j) * self.a_int

        self.assert_complex_equal(res, res_int)


class TestDiv(ComplexIntTests):
    """Tests for __truediv__ and __floordiv__"""

    def test_div(self):
        """Test complexint / complexint"""
        res = self.b / self.a
        res_int = self.b_int / self.a_int

        self.assert_complex_equal(res, res_int)

    def test_div_int(self):
        """Test complexint / int"""
        res = self.b / 3
        res_int = self.b_int / 3

        self.assert_complex_equal(res, res_int)

    def test_div_int_reversed(self):
        """Test int / complexint"""
        res = 10 / self.a
        res_int = 10 / self.a_int

        self.assert_complex_equal(res, res_int)

    def test_div_complex(self):
        """Test complexint / complex"""
        res = self.b / (1 + 2j)
        res_int = self.b_int / (1 + 2j)

        self.assert_complex_equal(res, res_int)

    def test_div_complex_reversed(self):
        """Test complex / complexint"""
        res = (2 + 4j) / self.a
        res_int = (2 + 4j) / self.a_int

        self.assert_complex_equal(res, res_int)


class TestPow(ComplexIntTests):
    """Tests for __pow__"""

    # TODO:
    # def test_power(self):
    #     res = self.b ** self.a
    #     res_int = self.b_int ** self.a_int
    #
    #     self.assertComplexEqual(res, res_int)

    def test_power_identity(self):
        """Test complexint ** 1"""
        res = self.b ** 1
        res_int = self.b_int ** 1

        self.assert_complex_equal(res, res_int)

    def test_power_int(self):
        """Test complexint ** int"""
        for i in range(3, 20):
            res = self.b ** i
            res_int = self.b_int ** i

            self.assert_complex_equal(res, res_int)

    # TODO:
    # def test_power_int_reversed(self):
    #     res = 10 ** self.a
    #     res_int = 10 ** self.a_int
    #
    #     self.assertComplexEqual(res, res_int)

    def test_power_int_negative(self):
        """Test complexint ** -int"""
        # This works, but... for anything other than (-1+0j) and (0-1j) it doesn't mean much to do this with integers,
        #   as that basically means to create a fraction, and this is for discrete maths!
        #
        # I'll leave this for now but I almost want to raise an error in this case (other than NotImplementedError)
        res = complex(0, -1) ** -5
        res_int = complexi(0, -1) ** -5

        self.assert_complex_equal(res, res_int)

    # TODO:
    #   This seems about as pointless as negative number powers
    # def test_power_complex(self):
    #     res = (36+29j) ** (9+1j)
    #     res_int = complexint(36, 29) ** (9+1j)
    #
    #     self.assertComplexEqual(res, res_int)

    # TODO:
    # def test_power_complex_reversed(self):
    #     res = (36+29j) ** (9+1j)
    #     res_int = (36+29j) ** complexint(9, 1)
    #
    #     self.assertComplexEqual(res, res_int)
