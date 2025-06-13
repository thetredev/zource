from zource import fibonacci


def test_fibonacci():
    impls = [
        fibonacci.nth_fibonacci_iterative,
        fibonacci.nth_fibonacci_recursive,
        fibonacci.nth_fibonacci_recursive_tail,
    ]
    for impl in impls:
        assert impl(9) == 34


def test_fibonacci_iterator():
    fibonacci_object = fibonacci.Fibonacci(10)
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # As iterator
    fibonacci_iter = iter(fibonacci_object)
    for expected_item in expected:
        actual = next(fibonacci_iter)
        assert actual == expected_item

    # As list
    fibonacci_list = list(fibonacci_object)
    for actual, expected_item in zip(fibonacci_list, expected, strict=False):
        assert actual == expected_item
