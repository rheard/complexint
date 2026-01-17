import numbers

from typing import Iterator, Tuple, Union

# Types that complexint operations are compatible with (other than complexint)
OTHER_OP_TYPES = Union[complex, int, float]
OP_TYPES = Union['complexint', OTHER_OP_TYPES]


def _square(ar: int, ai: int) -> Tuple[int, int]:
    """Square (ar+ai*i) using 2 big-int multiplies"""
    real = (ar - ai) * (ar + ai)
    imag = (ar * ai) << 1
    return real, imag


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
            return self.__class__(self.real + other.real, self.imag + other.imag)

        if isinstance(other, complex):
            return self.__class__(self.real + int(other.real), self.imag + int(other.imag))

        if isinstance(other, int):
            return self.__class__(self.real + other, self.imag)

        if isinstance(other, float):
            other = int(other)
            return self.__class__(self.real + other, self.imag)

        return NotImplemented

    def __radd__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__add__(other)

    def __sub__(self, other: OP_TYPES) -> 'complexint':
        if isinstance(other, complexint):
            return self.__class__(self.real - other.real, self.imag - other.imag)

        if isinstance(other, complex):
            return self.__class__(self.real - int(other.real), self.imag - int(other.imag))

        if isinstance(other, int):
            return self.__class__(self.real - other, self.imag)

        if isinstance(other, float):
            other = int(other)
            return self.__class__(self.real - other, self.imag)

        return NotImplemented

    def __rsub__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__neg__().__add__(other)

    def __neg__(self) -> 'complexint':
        return self.__class__(-self.real, -self.imag)

    def __pos__(self) -> 'complexint':
        return self.__class__(self.real, self.imag)

    def __mul__(self, other: OP_TYPES) -> 'complexint':
        if isinstance(other, complexint):
            a = self.real
            b = self.imag
            c = other.real
            d = other.imag

            return self.__class__(a * c - b * d, a * d + b * c)

        if isinstance(other, complex):
            a = self.real
            b = self.imag
            c = int(other.real)
            d = int(other.imag)

            return self.__class__(a * c - b * d, a * d + b * c)

        if isinstance(other, int):
            return self.__class__(self.real * other, self.imag * other)

        if isinstance(other, float):
            other = int(other)
            return self.__class__(self.real * other, self.imag * other)

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

            return self.__class__((self.real * oreal + self.imag * oimag) // d,
                                  (self.imag * oreal - self.real * oimag) // d)

        if isinstance(other, complex):
            # TODO: There may be additional tweaks or optimizations for integers
            oreal = int(other.real)
            oimag = int(other.imag)
            d = oreal * oreal + oimag * oimag

            if d == 0:
                raise ZeroDivisionError

            return self.__class__((self.real * oreal + self.imag * oimag) // d,
                                  (self.imag * oreal - self.real * oimag) // d)

        if isinstance(other, int):
            return self.__class__(self.real // other, self.imag // other)

        if isinstance(other, float):
            other = int(other)
            return self.__class__(self.real // other, self.imag // other)

        return NotImplemented

    def __rtruediv__(self, other: OTHER_OP_TYPES) -> 'complexint':
        if isinstance(other, int):
            new_other = self.__class__(real=other, imag=0)
            return new_other.__truediv__(self)

        if isinstance(other, float):
            other = int(other)
            new_other = self.__class__(real=other, imag=0)
            return new_other.__truediv__(self)

        if isinstance(other, complex):
            new_other = self.__class__(real=int(other.real), imag=int(other.imag))
            return new_other.__truediv__(self)

        return NotImplemented

    def __floordiv__(self, other: OP_TYPES) -> 'complexint':
        return self.__truediv__(other)

    def __rfloordiv__(self, other: OTHER_OP_TYPES) -> 'complexint':
        return self.__rtruediv__(other)

    def __pow__(self, power, modulo: None = None) -> 'complexint':  # noqa: ANN001
        if modulo is not None:
            raise TypeError("modulo argument not supported for this type")

        # accept only integers (or __index__-able); avoid float path
        try:
            e = power.__index__()  # avoids float; works for numpy ints too
        except AttributeError:
            if isinstance(power, (complexint, complex)):
                oreal = int(power.real)
                oimag = int(power.imag)

                if oreal == 0 and oimag == 0:
                    return self.__class__(1, 0)

                if self.real == 0 and self.imag == 0:
                    if oimag != 0 or oreal < 0:
                        raise ZeroDivisionError('0.0 to a negative or complex power') from None

                    return self.__class__(0, 0)

                # TODO: Add complex/complexint power
                #   The CPython source code uses a bunch of float methods like sin/atan2/etc...

                return NotImplemented

            if isinstance(power, float):
                e = int(power)
            else:
                return NotImplemented

        if e == 0:
            return self.__class__(1, 0)

        invert = e < 0
        if invert:
            e = -e

        rr = 1  # result.real
        ri = 0  # result.imag
        pr = self.real
        pi = self.imag

        # optional tiny fast paths (often hit in practice)
        if e == 1:
            res = self.__class__(pr, pi)
            return self.__class__(1, 0) / res if invert else res
        if e == 2:
            pr, pi = _square(pr, pi)
            res = self.__class__(pr, pi)
            return self.__class__(1, 0) / res if invert else res

        # bit-by-bit exponentiation
        while e:
            if e & 1:
                ac = rr * pr
                bd = ri * pi
                k = (rr + ri) * (pr + pi)
                rr, ri = ac - bd, k - ac - bd
            e >>= 1
            if e:  # avoid last unnecessary square
                pr, pi = _square(pr, pi)

        result = self.__class__(rr, ri)
        return self.__class__(1, 0) / result if invert else result

    def __abs__(self) -> 'complexint':
        return self.__class__(abs(self.real), abs(self.imag))

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

    def conjugate(self):
        """A recreation of the existing conjugate method"""
        return self.__class__(self.real, -self.imag)


C1 = complexint(1, 0)

numbers.Complex.register(complexint)
