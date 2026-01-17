This library provides a `complexint` class.

This class acts just like Python's built-in `complex` except it is backed by Python integers instead of doubles.
    This allows for infinite precision.

**WARNING**: This package has been deprecated. Please use [quadint](https://github.com/rheard/quadint) instead as below:

```python
from quadint import complexint

a = complexint(1, 2)
b = complexint(3, 6)

c = a * b
print(c)  # Outputs "-9+12j"

print(type(c.real))  # Outputs "int"
```

