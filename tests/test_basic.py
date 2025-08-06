"""These are simple tests to verify complexint acts very similar to complex, but just with int output"""

import unittest

from complexint import complexint


class TestPrecision(unittest.TestCase):

    def test_precision(self):
        """Test the purpose of this package: the difference in precision when compared to complex"""

        # This number + 1 (ending in 5) has too much precision to be stored in a double
        MISSING_NUM = 2397083434877565864

        a = complex(MISSING_NUM, 1)
        b = complex(MISSING_NUM, 1)
        c = complexint(MISSING_NUM, 1)

        b += 1  # Add 1 to b theoretically, but because double is limited, not actually changing the value
        self.assertEqual(a.real, b.real)

        c += 1  # Add 1 to c actually, getting a different value
        self.assertNotEqual(b.real, c.real)



class TestComplexInt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = complex(1, 2)
        cls.b = complex(3, 6)

        cls.a_int = complexint(1, 2)
        cls.b_int = complexint(3, 6)

    def assertComplexEqual(self, res, res_int):
        self.assertEquals(res.real, res_int.real)
        self.assertEquals(res.imag, res_int.imag)

        self.assertIsInstance(res_int.real, int)
        self.assertIsInstance(res_int.imag, int)


class TestAdd(TestComplexInt):

    def test_add(self):
        res = self.a + self.b
        res_int = self.a_int + self.b_int

        self.assertComplexEqual(res, res_int)

    def test_add_int(self):
        res = self.a + 10
        res_int = self.a_int + 10

        self.assertComplexEqual(res, res_int)

    def test_add_int_reversed(self):
        res = 10 + self.a
        res_int = 10 + self.a_int

        self.assertComplexEqual(res, res_int)

    def test_add_complex(self):
        res = self.a + (2+1j)
        res_int = self.a_int + (2+1j)

        self.assertComplexEqual(res, res_int)

    def test_add_complex_reversed(self):
        res = (2+1j) + self.a
        res_int = (2+1j) + self.a_int

        self.assertComplexEqual(res, res_int)


class TestSub(TestComplexInt):

    def test_sub(self):
        res = self.a - self.b
        res_int = self.a_int - self.b_int

        self.assertComplexEqual(res, res_int)

    def test_sub_int(self):
        res = self.a - 10
        res_int = self.a_int - 10

        self.assertComplexEqual(res, res_int)

    def test_sub_int_reversed(self):
        res = 10 - self.a
        res_int = 10 - self.a_int

        self.assertComplexEqual(res, res_int)

    def test_sub_complex(self):
        res = self.a - (2+1j)
        res_int = self.a_int - (2+1j)

        self.assertComplexEqual(res, res_int)

    def test_sub_complex_reversed(self):
        res = (2+1j) - self.a
        res_int = (2+1j) - self.a_int

        self.assertComplexEqual(res, res_int)


class TestNegPos(TestComplexInt):

    def test_neg(self):
        res = -self.a
        res_int = -self.a_int

        self.assertComplexEqual(res, res_int)

    def test_pos(self):
        res = +self.a
        res_int = +self.a_int

        self.assertComplexEqual(res, res_int)


class TestMul(TestComplexInt):

    def test_mul(self):
        res = self.a * self.b
        res_int = self.a_int * self.b_int

        self.assertComplexEqual(res, res_int)

    def test_mul_int(self):
        res = self.a * 10
        res_int = self.a_int * 10

        self.assertComplexEqual(res, res_int)

    def test_mul_int_reversed(self):
        res = 10 * self.a
        res_int = 10 * self.a_int

        self.assertComplexEqual(res, res_int)

    def test_mul_complex(self):
        res = self.a * (2+1j)
        res_int = self.a_int * (2+1j)

        self.assertComplexEqual(res, res_int)

    def test_mul_complex_reversed(self):
        res = (2+1j) * self.a
        res_int = (2+1j) * self.a_int

        self.assertComplexEqual(res, res_int)


class TestDiv(TestComplexInt):

    def test_div(self):
        res = self.b / self.a
        res_int = self.b_int / self.a_int

        self.assertComplexEqual(res, res_int)

    def test_div_int(self):
        res = self.b / 3
        res_int = self.b_int / 3

        self.assertComplexEqual(res, res_int)

    def test_div_int_reversed(self):
        res = 10 / self.a
        res_int = 10 / self.a_int

        self.assertComplexEqual(res, res_int)

    def test_div_complex(self):
        res = self.b / (1+2j)
        res_int = self.b_int / (1+2j)

        self.assertComplexEqual(res, res_int)

    def test_div_complex_reversed(self):
        res = (2+4j) / self.a
        res_int = (2+4j) / self.a_int

        self.assertComplexEqual(res, res_int)


class TestPow(TestComplexInt):

    # TODO:
    # def test_power(self):
    #     res = self.b ** self.a
    #     res_int = self.b_int ** self.a_int
    #
    #     self.assertComplexEqual(res, res_int)

    def test_power_int(self):
        res = self.b ** 3
        res_int = self.b_int ** 3

        self.assertComplexEqual(res, res_int)

    # TODO:
    # def test_power_int_reversed(self):
    #     res = 10 ** self.a
    #     res_int = 10 ** self.a_int
    #
    #     self.assertComplexEqual(res, res_int)

    # TODO
    # def test_power_int_negative(self):
    #     res = self.b ** -3
    #     res_int = self.b_int ** -3
    #
    #     self.assertComplexEqual(res, res_int)

