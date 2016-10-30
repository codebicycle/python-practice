import pytest

from iterator import squares_generator, squares_generator_expression
from iterator import squares_iterator_protocol

from iterator import fibonacci_generator, fibonacci_iterator_protocol


squares_implementations = [
    squares_generator,
    squares_generator_expression,
    squares_iterator_protocol,
]

@pytest.mark.parametrize('squares', squares_implementations)
def test_squares(squares):
    numbers = [1, 2, 3, 4, 5]
    it = squares(numbers)

    # Iterators are required to have an __iter__() method that returns the
    # iterator object itself so every iterator is also iterable and may be
    # used in most places where other iterables are accepted.
    assert iter(it) is it

    # Repeated calls to the iterator’s __next__() method (or passing it to
    # the built-in function next()) return successive items in the stream.
    assert list(it) == [n ** 2 for n in numbers]

    # When no more data are available a StopIteration exception is raised
    # instead. At this point, the iterator object is exhausted and any further
    # calls to its __next__() method just raise StopIteration again.
    assert list(it) == []
    assert list(it) == []

    assert iter(it) is it

    assert list(iter(it)) == []


fibonacci_implementations = [
    fibonacci_generator,
    fibonacci_iterator_protocol,
]

@pytest.mark.parametrize('fibonacci', fibonacci_implementations)
def test_fibonacci(fibonacci):
    it = fibonacci()

    # Iterators are required to have an __iter__() method that returns the
    # iterator object itself so every iterator is also iterable and may be
    # used in most places where other iterables are accepted.
    assert iter(it) is it

    # Repeated calls to the iterator’s __next__() method (or passing it to
    # the built-in function next()) return successive items in the stream.
    assert list(iter(it.__next__, 5)) == [1, 1, 2, 3]

    # Test that it goes on forever :P
    assert next(it) == 8

    assert iter(it) is it

