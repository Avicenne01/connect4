from __future__ import annotations

import functools
from multiprocessing.pool import ThreadPool
from typing import Callable, List, Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class COLORS:
    YELLOW = QColor(234, 207, 71)
    BLUE = QColor(41, 63, 132)
    RED = QColor(199, 43, 38)
    WHITE = Qt.white
    BLACK = Qt.black


def longest_sequence(array: List[int]) -> Tuple[int, int]:
    best = (0, 0)
    curr = (0, 0)

    for i, num in enumerate(array):
        start = i
        if num == array[curr[0]]:
            start = curr[0]
        curr = (start, i + 1)
        if num and curr[1] - curr[0] > best[1] - best[0]:
            best = curr

    return best


def timeout(seconds: Union[int, None]):
    """Timeout decorator. Given a work / task to perform, this decorator will raise
    a `TimeoutError` if the task takes too long.

    ## Usage::

        import time

        @timeout(2.0)
        def work():
            print('work started')
            time.sleep(3)
            print('work finished')
    """

    def timeout_decorator(work: Callable):
        @functools.wraps(work)
        def wrapper(*args, **kwargs):
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(work, args, kwargs)
            return async_result.get(seconds)

        return wrapper

    return timeout_decorator


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, value: Union[Point, int, float]) -> Point:
        if isinstance(value, Point):
            return Point(self.x + value.x, self.y + value.y)
        if isinstance(value, (int, float)):
            return Point(self.x + value, self.y + value)
        raise TypeError(
            "unsupported operand type(s) for +: {!r} and {!r}".format(
                self.__class__.__name__, type(value)
            )
        )

    def __mul__(self, value: Union[Point, int, float]) -> Point:
        if isinstance(value, Point):
            return Point(self.x * value.x, self.y * value.y)
        if isinstance(value, (int, float)):
            return Point(self.x * value, self.y * value)
        raise TypeError(
            "unsupported operand type(s) for *: {!r} and {!r}".format(
                self.__class__.__name__, type(value)
            )
        )

    def __str__(self) -> str:
        return "Point(x=%.2f, y=%.2f)" % (self.x, self.y)
