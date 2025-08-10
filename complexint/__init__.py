import numbers

from typing import Union


# Types that complexint operations are compatible with (other than complexint)
OTHER_OP_TYPES = Union[complex, int, float]
OP_TYPES = Union['complexint', OTHER_OP_TYPES]


class complexint:
    __slots__ = ('real', 'imag')
    real: int
    imag: int

    def __init__(self, real: int = 0, imag: int = 0):
        self.real = real
        self.imag = imag

    def __add__(self, other: OP_TYPES) -> 'complexint':
        if isinstance(other, complexint):
            return complexint(self.real + other.real, self.imag + other.imag)

        if isinstance(other, complex):
            return complexint(self.real + int(other.real), self.imag + int(other.imag))

        if isinstance(other, int):
            return complexint(self.real + other, self.imag)

        if isinstance(other, float):
            other = int(other)
            return complexint(self.real + other, self.imag)

        return NotImplemented

    def __radd__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__add__(other)

    def __sub__(self, other: OP_TYPES) -> 'complexint':
        if isinstance(other, complexint):
            return complexint(self.real - other.real, self.imag - other.imag)

        if isinstance(other, complex):
            return complexint(self.real - int(other.real), self.imag - int(other.imag))

        if isinstance(other, int):
            return complexint(self.real - other, self.imag)

        if isinstance(other, float):
            other = int(other)
            return complexint(self.real - other, self.imag)

        return NotImplemented

    def __rsub__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__neg__().__add__(other)

    def __neg__(self) -> 'complexint':
        return complexint(-self.real, -self.imag)

    def __pos__(self) -> 'complexint':
        return complexint(self.real, self.imag)

    def __mul__(self, other: OP_TYPES) -> 'complexint':
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

        if isinstance(other, int):
            return complexint(self.real * other, self.imag * other)

        if isinstance(other, float):
            other = int(other)
            return complexint(self.real * other, self.imag * other)

        return NotImplemented

    def __rmul__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__mul__(other)

    def __truediv__(self, other: OP_TYPES) -> 'complexint':
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

        if isinstance(other, int):
            return complexint(self.real // other, self.imag // other)

        if isinstance(other, float):
            other = int(other)
            return complexint(self.real // other, self.imag // other)

        return NotImplemented

    def __rtruediv__(self, other: OTHER_OP_TYPES) -> 'complexint':
        if isinstance(other, int):
            other = complexint(real=other, imag=0)
            return other.__truediv__(self)

        if isinstance(other, float):
            other = int(other)
            other = complexint(real=other, imag=0)
            return other.__truediv__(self)

        if isinstance(other, complex):
            other = complexint(real=int(other.real), imag=int(other.imag))
            return other.__truediv__(self)

        return NotImplemented

    def __floordiv__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__truediv__(other)

    def __rfloordiv__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__rtruediv__(other)

    def __pow__(self, power: OP_TYPES, modulo: None = None) -> 'complexint':
        if modulo is not None:
            raise TypeError("modulo argument not supported for this type")

        if isinstance(power, (int, float)):
            # TODO: This is probably sub-optimal,
            #   but the CPython source code uses a bunch of float methods like sin/atan2/etc...
            power = int(power)

            if power == 0:
                return C1

            invert = power < 0
            if invert:
                power = -power

            base = self
            result = C1
            while power:
                if power & 1:
                    result *= base
                base *= base
                power >>= 1

            return C1 / result if invert else result

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

    def __abs__(self) -> 'complexint':
        return complexint(abs(self.real), abs(self.imag))

    def __repr__(self) -> str:
        parens = self.real == 0

        lead = "(" if parens else ""
        tail = ")" if parens else ""

        op = "+" if self.imag >= 0 else "-"

        real = self.real or ""
        imag = abs(self.imag)

        return f"{lead}{real}{op}{imag}j{tail}"

    def __str__(self) -> str:
        return self.__repr__()


C1 = complexint(1, 0)

numbers.Complex.register(complexint)
