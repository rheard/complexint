This library provides a `complexint` class.

This class acts just like Python's built-in `complex` except it is backed by Python integers instead of doubles.
    This allows for infinite precision.

## Example

```python
from complexint import complexint

a = complexint(1, 2)
b = complexint(3, 6)

c = a * b
print(c)  # Outputs "-9+12j"

print(type(c.real))  # Outputs "int"
```

## Disclaimer

This is intended for use with discrete mathematics, and ideally will be limited to the
    operations: add, sub, mul, and pow.

Trying to divide using this class, or using floats with this class, will result in integer conversion cutoff.

As an example of this problem, note the equivalences below:
```python
from complexint import complexint

a = complexint(3, 6)

print(a / 3)  # Outputs "1+2j
print(a / 3.5)  # Outputs "1+2j"

print(a + 1)  # Outputs "4+6j"
print(a + 1.5)  # Outputs "4+6j"
```