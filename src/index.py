import random as rd

from PyQt5.QtCore import QThread

from models.player import Player, PlayerIterator
from models.token import Tokens
from signals import default_signals
from src.game import Game, GameSettings
from src.ui import Connect4UI


class Connect4:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        settings=GameSettings(),
        random_start=False,
    ) -> None:
        self._players = [player1, player2]
        self.random_start = random_start
        self.init()

        self.signals = default_signals
        self.game = Game(
            use_player=self.use_player, signals=self.signals, settings=settings
        )
        self.ui = Connect4UI(
            use_player=self.use_player, signals=self.signals, settings=settings
        )

    def init(self):
        if self.random_start and rd.random() > 0.5:
            self._players.reverse()

        # set players token.
        self._players[0].token = Tokens.RED
        self._players[1].token = Tokens.YELLOW

        self.players = iter(PlayerIterator(*self._players))
        self.current_player = next(self.players)

    def use_player(self):
        def _get_current_player() -> Player:
            return self.current_player

        return self._players, _get_current_player

    def reset(self):
        self.init()
        self.game.reset()
        # TODO: update UI or emit a `restart_game` event

    def play(self, col: int):
        pos = self.game.play(col)
        if pos:
            self.ui.play(pos)
            self.current_player = next(self.players)

    def run(self):
        self.reset()
        self.thread = QThread()
        self.game.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.game.run)
        self.signals.mouse_moved.connect(self.ui.board.highlightColumn)
        self.signals.column_choosed.connect(self.play)
        self.signals.game_over.connect(self.ui.gameOver)

        self.signals.game_over.connect(self.thread.quit)
        self.signals.game_over.connect(self.game.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.ui.show()
