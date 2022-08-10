import logging
import platform
import sys

from PyQt5.QtWidgets import QApplication

from ai.alphabeta_player import AlphaBetaPlayer
from src.game import GameSettings
from src.index import Connect4
from src.logger import logger
from src.models.player import HumanPlayer  # , RandomPlayer

# Add QT plugin path to environment for windows platform
if platform.system().lower() == "windows":
    import os
    import PyQt5
    
    pyqt = os.path.dirname(PyQt5.__file__)
    os.environ['QT_PLUGIN_PATH'] = os.path.join(pyqt, "Qt/plugins")

if __name__ == "__main__":
    player1 = HumanPlayer("Player1")
    player2 = AlphaBetaPlayer(depth=3)
    settings = GameSettings()

    app = QApplication(sys.argv)

    args = sys.argv[1:]
    logger.setLevel(logging.INFO)
    if len(args) == 1 and args[0] == "--debug":
        logger.setLevel(logging.DEBUG)
        settings.timeout_secs = None

    logger.info("Starting the Connect4 app...")
    connect4 = Connect4(player1, player2, settings)
    connect4.run()
    sys.exit(app.exec_())
