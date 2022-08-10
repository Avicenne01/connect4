import multiprocessing
import time
from dataclasses import dataclass

from PyQt5.QtCore import QObject

import utils
from models import UseState
from models.board import Board
from models.player import Player
from signals import Signals
from src.logger import logger

SLEEP_SECS = 0.2


def sleep():
    logger.debug("sleeping for %s ms" % (SLEEP_SECS * 1_000))
    time.sleep(SLEEP_SECS)


@dataclass
class GameSettings:
    grid_nrows: int = 6
    grid_ncols: int = 7
    winning_length: int = 4
    timeout_secs: float = 0.5


class Game(QObject):
    def __init__(
        self,
        use_player: UseState,
        signals: Signals,
        settings=GameSettings(),
    ):
        super().__init__()
        self.board = Board(
            nrows=settings.grid_nrows,
            ncols=settings.grid_ncols,
            winning_length=settings.winning_length,
        )
        self.timeout_secs = settings.timeout_secs
        self._players, self.get_current_player = use_player()
        self.signals = signals
        self.create_get_next_move()
        self.reset()

    @property
    def winner(self):
        token_value = self.board.winner_token_value
        if token_value is None:
            return None
        return self.get_player_from_token(token_value)

    @property
    def winning_cells(self):
        return self.board.winning_cells

    def reset(self):
        self.board.reset()

    def create_get_next_move(self):
        if self.timeout_secs:
            logger.info(
                "Non human player strategy will timeout after %ss" % self.timeout_secs
            )

        @utils.timeout(self.timeout_secs)
        def get_next_move(player: Player):
            return player.strategy(self.board)

        self.get_next_move = get_next_move

    def get_player_from_token(self, token_value: int):
        for player in self._players:
            if player.token.value == token_value:
                return player

    def is_over(self):
        return self.board.is_leaf()

    def make_current_player_lose(self):
        winner = None
        current_player = self.get_current_player()
        for player in self._players:
            if player is not current_player:
                winner = player
                break
        self.signals.game_over.emit(winner.name, self.winning_cells)

    def play(self, col: int):
        if col is None:
            # This happens when human player click outside of the grid
            return

        row = self.board.play(self.get_current_player().token.value, col)
        pos = (col, row)
        if pos not in self.board:
            return
        logger.debug(
            "Board capacity = %s, winner_token = %s"
            % (self.board.capacity, self.board.winner_token_value)
        )
        return pos

    def run(self):
        while not self.is_over():
            if self.get_current_player().is_human:
                # If HUMAN, then wait for manual play
                sleep()
                continue

            try:
                col = self.get_next_move(self.get_current_player())
                self.signals.column_choosed.emit(col)
                sleep()
            except multiprocessing.context.TimeoutError:
                logger.error("%s took too long !" % self.get_current_player().name)
                self.make_current_player_lose()
                return

        logger.debug("Game over")
        winner = self.winner
        if winner:
            winner = winner.name
        self.signals.game_over.emit(winner, self.winning_cells)
