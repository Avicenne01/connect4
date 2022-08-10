import random as rd
from typing import List

from models.board import Board
from models.token import Token, Tokens


class Player:
    is_human = False
    token = Tokens.EMPTY

    def __init__(self, name=""):
        self.name = name

    def set_token(self, token: Token):
        self.token = token

    def strategy(self, board: Board) -> int:
        """Implements the strategy for the player.

        Args
        ----
            board: `models.board.Board`\n
                The current state of the game board

        Returns
        -------
            col: `int`, `range(0, board.ncols)`\n
                Column where to play the token
        """
        raise NotImplementedError("Player strategy not implemented.")


class HumanPlayer(Player):
    is_human = True

    def strategy(self, board: Board):
        ncols = board.ncols
        column = input(
            "%s it's your turn. Choose a column (valid range 1 - %s): "
            % (self.name, ncols)
        )

        def valid_column(column: str):
            return column.isnumeric() and 0 < int(column) <= ncols

        while not valid_column(column):
            column = input(
                "%s it's your turn. Choose a column (valid range 1 - %s): "
                % (self.name, ncols)
            )
        return int(column) - 1


class RandomPlayer(Player):
    def strategy(self, board: Board):
        columns = board.get_available_columns()
        if columns:
            col = rd.choice(columns)
            return col


class PlayerIterator:
    def __init__(self, *players) -> None:
        self.players: List[Player] = players[:]
        self.length = len(self.players)

    def __next__(self):
        player = self.players[self.current]
        self.current = (self.current + 1) % self.length
        return player

    def __iter__(self):
        self.current = 0
        return self
