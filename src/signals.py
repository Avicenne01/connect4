from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal


class Signal(QObject):
    trigger: pyqtSignal

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def emit(self, *args):
        self.trigger.emit(*args)

    def connect(self, receiver: Callable):
        self.trigger.connect(receiver)


class ColumnChoosed(Signal):
    name = "column_choosed"
    trigger = pyqtSignal(int, name=name)


class MouseMoved(Signal):
    name = "mouse_moved"
    trigger = pyqtSignal(int, name=name)


class GameOver(Signal):
    name = "game_over"
    trigger = pyqtSignal(str, list, name=name)


class RestartGame(Signal):
    name = "restart_game"
    trigger = pyqtSignal(name=name)


class Signals:
    def __init__(self, *signals) -> None:
        self._signals: dict[str, Signal] = {}
        self.add(*signals)

    def add(self, *signals) -> None:
        for signal in signals:
            self._signals[signal.name] = signal

    def get(self, name: str, default=None):
        return self._signals.get(name, default)

    def __getattr__(self, attr: str):
        if attr in self._signals:
            return self._signals.get(attr)
        raise AttributeError("attributes '%s' not found" % attr)

    def __contains__(self, name: str) -> bool:
        return name in self._signals


default_signals = Signals(MouseMoved(), ColumnChoosed(), GameOver(), RestartGame())
