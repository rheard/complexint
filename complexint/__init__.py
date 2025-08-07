import numbers


class complexint:
    __slots__ = ('real', 'imag')
    real: int
    imag: int

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        if isinstance(other, complexint):
            return complexint(self.real + other.real, self.imag + other.imag)

        if isinstance(other, complex):
            return complexint(self.real + int(other.real), self.imag + int(other.imag))

        if isinstance(other, (int, float)):
            if isinstance(other, float):
                other = int(other)

            return complexint(self.real + other, self.imag)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, complexint):
            return complexint(self.real - other.real, self.imag - other.imag)

        if isinstance(other, complex):
            return complexint(self.real - int(other.real), self.imag - int(other.imag))

        if isinstance(other, (int, float)):
            return complexint(self.real - int(other), self.imag)

        return NotImplemented

    def __rsub__(self, other):
        return self.__neg__().__add__(other)

    def __neg__(self):
        return complexint(-self.real, -self.imag)

    def __pos__(self):
        return complexint(self.real, self.imag)

    def __mul__(self, other):
        if isinstance(other, (complexint, complex)):
            a = self.real
            b = self.imag
            if isinstance(other, complex):
                c = int(other.real)
                d = int(other.imag)
            else:
                c = other.real
                d = other.imag

            ac = a*c
            bd = b*d
            ad = a*d
            bc = b*c

            return complexint(ac - bd, ad + bc)

        if isinstance(other, (int, float)):
            other = int(other)
            return complexint(self.real * other, self.imag * other)

        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (complexint, complex)):
            # TODO: I would not trust this...
            #   I copied the cpython source code (the non-optimal version at that),
            #   but there may be additional tweaks or optimizations for integers
            if isinstance(other, complex):
                oreal = int(other.real)
                oimag = int(other.imag)
            else:
                oreal = other.real
                oimag = other.imag

            d = oreal * oreal + oimag * oimag

            if d == 0:
                raise ZeroDivisionError

            return complexint((self.real * oreal + self.imag * oimag) // d,
                              (self.imag * oreal - self.real * oimag) // d)

        if isinstance(other, (int, float)):
            other = int(other)
            return complexint(self.real // other, self.imag // other)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            other = complexint(real=other, imag=0)
            return other.__truediv__(self)

        if isinstance(other, complex):
            other = complexint(real=int(other.real), imag=int(other.imag))
            return other.__truediv__(self)

        return NotImplemented

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __rfloordiv__(self, other):
        return self.__rtruediv__(other)

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            raise TypeError("modulo argument not supported for this type")

        if isinstance(power, (int, float)):
            # TODO: This is probably sub-optimal,
            #   but the CPython source code uses a bunch of float methods like sin/atan2/etc...
            if power < 0:
                return C1 / self.__pow__(-power)

            def rec(x, n):
                if n == 0:
                    return 1  # multiplicative identity; matches your current behavior
                if n == 1:
                    return x
                half = rec(x, n // 2)
                result = half * half
                if n & 1:  # if n is odd
                    result = result * x
                return result

            return rec(self, power)

        if isinstance(power, (complexint, complex)):
            oreal = int(power.real)
            oimag = int(power.imag)

            if oreal == 0 and oimag == 0:
                return complexint(1, 0)

            if self.real == 0 and self.imag == 0:
                if oimag != 0 or oreal < 0:
                    raise ZeroDivisionError('0.0 to a negative or complex power')

                return complexint(0, 0)

            # TODO: Add complex/complexint power
            #   The CPython source code uses a bunch of float methods like sin/atan2/etc...

        return NotImplemented

    def __abs__(self):
        return complexint(abs(self.real), abs(self.imag))

    def __repr__(self):
        parens = self.real == 0

        lead = "(" if parens else ""
        tail = ")" if parens else ""

        op = "+" if self.imag >= 0 else "-"

        real = self.real or ""
        imag = abs(self.imag)

        return f"{lead}{real}{op}{imag}j{tail}"

    def __str__(self):
        return self.__repr__()


C1 = complexint(1, 0)

numbers.Complex.register(complexint)
