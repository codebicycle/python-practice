"""
A look at Python's iterator protocol.

Required reading:

https://docs.python.org/3/glossary.html#term-iterator
https://docs.python.org/3/glossary.html#term-iterable
https://docs.python.org/3/library/stdtypes.html#typeiter
https://docs.python.org/3/reference/datamodel.html#object.__iter__

https://docs.python.org/3/library/functions.html#iter
https://docs.python.org/3/library/functions.html#next

More details on generators:

https://docs.python.org/3/glossary.html#term-generator
https://docs.python.org/3/glossary.html#term-generator-iterator
https://docs.python.org/3/reference/expressions.html#generator.__next__
https://docs.python.org/3/glossary.html#term-generator-expression
https://docs.python.org/3.6/reference/expressions.html#generator-expressions

"""

class SquareIterator:

    def __init__(self, iterable):
        self.iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator) ** 2


class FibonacciIterator:

    def __init__(self):
        self.a = 1
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        fibonacci = self.a
        self.a, self.b = self.b, self.a + self.b
        return fibonacci


def squares_generator(numbers):
    """Given an iterable of numbers, return an iterator that returns their
    squares.

    """
    for n in numbers:
        yield n ** 2


def squares_generator_expression(numbers):
    """Given an iterable of numbers, return an iterator that returns their
    squares.

    """
    return (n ** 2 for n in numbers)


def squares_iterator_protocol(numbers):
    """Given an iterable of numbers, return an iterator that returns their
    squares.

    """
    # More specifically, return an object conforming to the iterator protocol
    # that is not a generator iterator.

    return SquareIterator(numbers)


def fibonacci_generator():
    """Return an iterator that returns all the Fibonacci numbers, forever."""
    a = 1
    b = 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_iterator_protocol():
    """Return an iterator that returns all the Fibonacci numbers, forever."""

    # More specifically, return an object conforming to the iterator protocol
    # that is not a generator iterator.

    return FibonacciIterator()
