from copy import deepcopy
from typing import Dict, List, Tuple, Union

from PyQt5.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QMouseEvent, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QLabel,
    QWidget,
)

from game import GameSettings
from models import UseState
from signals import Signals
from utils import COLORS, Point

Position = Tuple[int, int]


class Connect4UI(QWidget):
    title = "Connect 4 game"
    w_width = 800  # window width
    w_height = 600  # window height

    def __init__(
        self,
        use_player: UseState,
        signals: Signals,
        settings=GameSettings(),
        parent=None,
    ):
        super().__init__(parent)
        self.use_player = use_player
        self.signals = signals
        self.nrows = settings.grid_nrows
        self.ncols = settings.grid_ncols

        self.board = Connect4Board(self)

        self.game_over = False
        self.uiSetup()

    def reset(self):
        self.game_over = False
        self.board.clear()

    def uiSetup(self):
        players, _ = self.use_player()

        # window general setup
        self.setWindowTitle(self.title)
        self.setFixedWidth(self.w_width)
        self.setFixedHeight(self.w_height)

        # create window layout
        self.gameOverLabel = QLabel()
        self.gameOverLabel.setFont(QFont("Helvetica", 30, QFont.Bold))
        self.gameOverLabel.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.player_1 = Connect4Player(
            self, name=players[0].name, color=players[0].token.color
        )
        self.player_2 = Connect4Player(
            self, name=players[1].name, color=players[1].token.color
        )

        self.layout.addWidget(self.gameOverLabel, 0, 0, 1, 4)
        self.layout.addWidget(self.player_1, 2, 0, 1, 2)
        self.layout.addWidget(self.player_2, 4, 0, 1, 2)
        self.layout.addWidget(self.board, 1, 1, 6, 3)

        self.setLayout(self.layout)

    def play(self, pos: Position):
        _, get_current_player = self.use_player()
        color = get_current_player().token.color
        ui_pos = (pos[0], self.nrows - 1 - pos[1])
        # self.board.addToken(ui_pos, color)
        self.board.dropToken(ui_pos, color)

    def gameOver(self, winner: Union[str, None], winning_cells: List[Position]):
        self.game_over = True
        msg = f"{winner} won." if winner else "It's a draw."
        self.gameOverLabel.setText("Game over ! " + msg)
        self.board.setGameOver(self.game_over)
        self.board.highlightWinningCells(winning_cells)


class Connect4Player(QWidget):
    p_width = 200
    p_height = 100

    def __init__(self, parent=None, name="Player", color=COLORS.BLACK):
        super().__init__(parent)
        self.name = name
        self.color = color

        self.setFixedWidth(self.p_width)
        self.setFixedHeight(self.p_height)
        self.name_label = QLabel("<h2>%s</h2>" % (self.name), self)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(self.color, -1, Qt.SolidLine))
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))

        # draw token
        disc_size = 40
        margin_top = 30
        margin_left = 10
        painter.drawEllipse(margin_left, margin_top, disc_size, disc_size)


class Connect4Board(QFrame):
    f_width = 550  # frame width
    f_height = 500  # frame height
    margin = 20
    cell_margin = 3

    def __init__(
        self,
        parent: Connect4UI,
    ):
        super().__init__(parent)
        self.signals = parent.signals
        _, self.get_current_player = parent.use_player()
        self.nrows = parent.nrows
        self.ncols = parent.ncols
        self.cell_size = (self.f_width - 2 * self.margin) // self.ncols

        self.setFixedWidth(self.f_width)
        self.setFixedHeight(self.f_height)
        self.setMouseTracking(True)  # need this to trigger mouseMoveEvent

        self.game_over = False
        self.h_col = None  # highlighted col
        self.h_color = None  # highlighted col color

        self.reset()

    def clear(self):
        self.reset()
        self.update()

    def reset(self):
        self.resetTokens()
        self.resetDropTokens()

    def resetTokens(self):
        self.tokens = {}
        for i in range(self.ncols):
            for j in range(self.nrows):
                self.tokens[(i, j)] = Qt.white

    def resetDropTokens(self):
        self.cells: Dict[Position, QWidget] = {}
        self.anims: Dict[Position, QPropertyAnimation] = {}
        radius = self.cell_size
        width = radius - 2 * self.cell_margin
        width2 = width * 1.1
        shift = self.margin + self.cell_margin
        for i in range(self.ncols):
            for j in range(self.nrows):
                x = i * radius + shift
                y = j * radius + shift
                cell = QWidget(self)
                cell.resize(width, width)
                cell.move(x, 0)
                self.cells[(i, j)] = cell
                # bounce anim
                anim = QPropertyAnimation(cell, b"pos")
                anim.setEasingCurve(QEasingCurve.OutBounce)
                anim.setEndValue(QPoint(x, y))
                anim.setDuration((j + 1) * 50)
                self.anims[(i, j)] = anim

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, -1, Qt.SolidLine))
        self.drawGrid(painter)

    def drawGrid(self, painter: QPainter):
        # set grid background
        grid_background = QBrush(COLORS.BLUE, Qt.SolidPattern)
        painter.setBrush(grid_background)

        grid_width = self.ncols * self.cell_size
        grid_height = self.nrows * self.cell_size
        painter.drawRect(self.margin, self.margin, grid_width, grid_height)

        for i in range(self.ncols):
            for j in range(self.nrows):
                self.drawToken(painter, (i, j), self.tokens[(i, j)])

        if self.h_col is not None and self.h_col < self.ncols:
            painter.setBrush(QBrush(self.h_color, Qt.Dense4Pattern))
            painter.drawRect(
                self.margin + self.h_col * self.cell_size,
                self.margin,
                self.cell_size,
                grid_height,
            )

    def drawGridLines(self, painter: QPainter):
        thickness = 3
        painter.setPen(QPen(Qt.black, thickness, Qt.SolidLine))

        # draw vertical lines
        for i in range(1, self.ncols):
            painter.drawLine(
                self.margin + i * self.cell_size,
                self.margin + thickness * 2,
                self.margin + i * self.cell_size,
                self.nrows * self.cell_size + self.margin - thickness * 2,
            )

        # draw horizontal lines
        for j in range(1, self.nrows):
            painter.drawLine(
                self.margin + thickness * 2,
                self.margin + j * self.cell_size,
                self.ncols * self.cell_size + self.margin - thickness * 2,
                self.margin + j * self.cell_size,
            )

        # restore painter
        painter.setPen(QPen(Qt.black, -1, Qt.SolidLine))

    def drawToken(self, painter: QPainter, pos: tuple, color: QColor):
        # set token color
        painter.setBrush(QBrush(color, Qt.SolidPattern))

        # get circle parameters
        radius = self.cell_size
        shift = self.margin + self.cell_margin
        width = radius - 2 * self.cell_margin
        height = width
        center = Point(*pos) * radius + shift

        painter.drawEllipse(center.x, center.y, width, height)

    def dropToken(self, pos: Position, color: QColor):
        # print("Will drop token at position", pos, "and color:", color.name())
        cell = self.cells[pos]
        width = self.cell_size - 2 * self.cell_margin
        cell.setStyleSheet(
            "background-color:%s;border-radius:%spx;border:2px solid white;"
            % (color.name(), width / 2)
        )

        effect = QGraphicsDropShadowEffect()
        effect.setColor(Qt.white)
        effect.setOffset(1, 1.5)
        effect.setBlurRadius(10)
        cell.setGraphicsEffect(effect)
        self.anims[pos].start()

    def mousePressEvent(self, event: QMouseEvent):
        if self.game_over:
            return super().mousePressEvent(event)

        x = event.x()
        if x < self.margin or x > self.f_width - self.margin:
            return
        col = (x - self.margin) // self.cell_size
        if self.get_current_player().is_human:
            self.signals.column_choosed.emit(col)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.game_over:
            return super().mouseMoveEvent(event)
        x = event.x()
        if x < self.margin or x > self.f_width - self.margin:
            return
        col = (x - self.margin) // self.cell_size
        self.signals.mouse_moved.emit(col)

    def highlightColumn(self, col: int):
        color = self.get_current_player().token.color
        color = deepcopy(color)
        color.setAlpha(150)
        self.h_col = col
        self.h_color = color
        self.update()

    # def addToken(self, pos: tuple, color: QColor):
    #     self.tokens[pos] = color
    #     self.update()

    def setGameOver(self, value: bool):
        self.game_over = value

    def highlightWinningCells(self, winning_cells: List[Position]):
        winning_ui_cells = [(pos[0], self.nrows - 1 - pos[1]) for pos in winning_cells]
        for pos in winning_ui_cells:
            cell = self.cells[pos]
            width = (self.cell_size - 2 * self.cell_margin) * 1.1
            width = int(width)
            cell.resize(width, width)
            style = cell.styleSheet()
            cell.setStyleSheet(
                style
                + "border-radius:%spx;border:2px solid rgb(0, 255, 0);" % (width / 2)
            )
