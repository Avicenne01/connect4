from typing import List, Tuple, Union

import utils
from src.logger import logger

from models.token import Tokens

Position = Tuple[int, int]


class Board:
    def __init__(self, nrows=6, ncols=7, winning_length=4):
        self.nrows = nrows
        self.ncols = ncols
        self.winning_length = winning_length
        self.capacity = nrows * ncols
        self.reset()
        logger.debug(f"Created {self!r}")

    def reset(self):
        self.reset_winner()
        self.board = [[0] * self.nrows for _ in range(self.ncols)]
    
    def reset_winner(self):
        self.winner_token_value = None
        self.winning_cells: Tuple[int, int] = []

    def get_row(self, i: int):
        # TODO
        pass

    def get_col(self, j: int):
        positions = [(j, i) for i in range(self.nrows)]
        return self.board[j], positions

    def get_diagonal(self, up: bool, shift: int):
        # TODO
        pass

    def get_height(self, col: int):
        # TODO
        pass

    def get_available_columns(self):
        # TODO
        pass

    def is_full(self):
        return self.capacity == 0

    def is_leaf(self):
        return (self.winner_token_value is not None) or self.is_full()

    def play(self, token_value: int, col: int):
        if col >= self.ncols or col < 0 or token_value not in {1, -1}:
            logger.debug("Cannot play token in column %d" % col)
            return -1

        row = self.get_height(col)
        if row < self.nrows:
            self.board[col][row] = token_value
            self.capacity -= 1
            logger.debug("Played token=%d at col=%d, row=%d" % (token_value, col, row))
            self.check_for_winner(pos=(col, row))
            return row
        return -1

    def cancel_play(self, token_value: int, col: int):
        if col >= self.ncols or col < 0 or token_value not in {1, -1}:
            raise ValueError("invalid arguments.")

        row = self.get_height(col)
        if row == 0:
            raise Exception(
                "cannot cancel play at column %d. Reason: column was previously empty."
                % col
            )
        if self.board[col][row - 1] != token_value:
            raise Exception(
                "cannot cancel play at column %d. Reason: expected token_value to be %d."
                % (col, token_value)
            )
        self.board[col][row - 1] = 0
        self.capacity += 1
        self.reset_winner()

    def check_for_winner(self, pos: Position):
        if not pos in self:
            logger.debug("Skipping winner check for pos=(%d, %d)" % pos)
            return
        logger.debug("Checking for winner in sequences having pos=(%d, %d)" % pos)
        sequences = [
            self.get_col(pos[0]),
            self.get_row(pos[1]),
            self.get_diagonal(up=True, shift=pos[0] - pos[1]),
            self.get_diagonal(up=False, shift=pos[0] + pos[1]),
        ]
        for values, positions in sequences:
            start, end = utils.longest_sequence(values)
            token_value = values[start]
            length = end - start
            if length >= self.winning_length:
                self.winner_token_value = token_value
                self.winning_cells = [positions[i] for i in range(start, end)]
                logger.debug("Found winner !")
                break
        if not self.winner_token_value:
            logger.debug("No winner found")

    def __contains__(self, position: Position):
        j, i = position
        return 0 <= i < self.nrows and 0 <= j < self.ncols

    def __getitem__(self, key: Union[Position, int]):
        if isinstance(key, tuple) and key in self:
            j, i = key
            return self.board[j][i]
        elif isinstance(key, int) and 0 <= key < self.ncols:
            return self.board[key]
        else:
            raise KeyError(f"{key} not in {self!r}")

    def __str__(self):
        rows = []
        for i in range(self.nrows):
            tokens, _ = self.get_row(i)
            rows.append("|%s|" % "|".join(map(lambda x: Tokens.get_display(x), tokens)))
        return "\n".join(reversed(rows))

    def __repr__(self):
        return f"<Board nrows={self.nrows} ncols={self.ncols} capacity={self.capacity}>"
