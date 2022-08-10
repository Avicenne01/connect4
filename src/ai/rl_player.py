from models.board import Board
from models.player import Player

infty = float("inf")


class RLPlayer(Player):
    def __init__(self, name="MY_AI_NAME"):
        super().__init__(name)

    def strategy(self, board: Board):
        # TODO
        pass
