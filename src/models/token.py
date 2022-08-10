from PyQt5.QtGui import QColor

from utils import COLORS


class Token:
    def __init__(self, value: int, display: str, color: QColor) -> None:
        self.value = value
        self.display = display
        self.color = color


class Tokens:
    _value_to_display = {-1: "x", 0: " ", 1: "o"}
    EMPTY = Token(value=0, display=" ", color=COLORS.WHITE)
    RED = Token(value=1, display="o", color=COLORS.RED)
    YELLOW = Token(value=-1, display="x", color=COLORS.YELLOW)

    @classmethod
    def get_display(cls, value: int) -> str:
        return cls._value_to_display[value]
