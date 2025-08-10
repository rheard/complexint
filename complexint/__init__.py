import numbers

from typing import Iterator, Union

# Types that complexint operations are compatible with (other than complexint)
OTHER_OP_TYPES = Union[complex, int, float]
OP_TYPES = Union['complexint', OTHER_OP_TYPES]


class complexint:
    """
    Represents a complex number with integer real and imaginary parts.

    Attributes:
        real (int): The real component.
        imag (int): The imaginary component.
    """

    __slots__ = ('real', 'imag')
    real: int
    imag: int

    def __init__(self, real: int = 0, imag: int = 0):
        """
        Initialize a complexint instance.

        Args:
            real (int, optional): The real part of the number. Defaults to 0.
            imag (int, optional): The imaginary part of the number. Defaults to 0.
        """
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
        if isinstance(other, complexint):
            a = self.real
            b = self.imag
            c = other.real
            d = other.imag

            return complexint(a * c - b * d, a * d + b * c)

        if isinstance(other, complex):
            a = self.real
            b = self.imag
            c = int(other.real)
            d = int(other.imag)

            return complexint(a * c - b * d, a * d + b * c)

        if isinstance(other, int):
            return complexint(self.real * other, self.imag * other)

        if isinstance(other, float):
            other = int(other)
            return complexint(self.real * other, self.imag * other)

        return NotImplemented

    def __rmul__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__mul__(other)

    def __truediv__(self, other: OP_TYPES) -> 'complexint':
        if isinstance(other, complexint):
            # TODO: There may be additional tweaks or optimizations for integers
            oreal = other.real
            oimag = other.imag
            d = oreal * oreal + oimag * oimag

            if d == 0:
                raise ZeroDivisionError

            return complexint((self.real * oreal + self.imag * oimag) // d,
                              (self.imag * oreal - self.real * oimag) // d)

        if isinstance(other, complex):
            # TODO: There may be additional tweaks or optimizations for integers
            oreal = int(other.real)
            oimag = int(other.imag)

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
            new_other = complexint(real=other, imag=0)
            return new_other.__truediv__(self)

        if isinstance(other, float):
            other = int(other)
            new_other = complexint(real=other, imag=0)
            return new_other.__truediv__(self)

        if isinstance(other, complex):
            new_other = complexint(real=int(other.real), imag=int(other.imag))
            return new_other.__truediv__(self)

        return NotImplemented

    def __floordiv__(self, other: OP_TYPES) -> 'complexint':
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

            br, bi = self  # base
            rr, ri = C1  # result
            while power:
                if power & 1:
                    rr, ri = rr * br - ri * bi, rr * bi + ri * br
                power >>= 1
                if power:
                    br, bi = br * br - bi * bi, (br * bi) << 1

            result = complexint(rr, ri)
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

    def __iter__(self) -> Iterator:
        return iter((self.real, self.imag))

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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (complexint, complex)):
            return self.real == other.real and self.imag == other.imag

        if isinstance(other, (float, int)):
            return self.imag == 0 and self.real == other

        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.real, self.imag))

    def __bool__(self) -> bool:
        return (self.real | self.imag) != 0


C1 = complexint(1, 0)

numbers.Complex.register(complexint)
