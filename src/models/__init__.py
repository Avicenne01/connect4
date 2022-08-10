from typing import Callable, List, Tuple

from models.player import Player

Getter = Callable[[], Player]

UseState = Callable[[], Tuple[List[Player], Getter]]
