import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtNetwork import QAbstractSocket, QTcpSocket
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSvgWidgets import QSvgWidget

import chess
import chess.svg


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.socket = QTcpSocket(self)
        self.buffer = b""

        self.board_widget = QSvgWidget()
        self.setCentralWidget(self.board_widget)

        self.setWindowTitle("Chess Bot")
        self.setFixedSize(480, 480)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.socket.readyRead.connect(self.read_fen_updates)
        self.socket.errorOccurred.connect(self.schedule_reconnect)

        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setInterval(1000)
        self.reconnect_timer.timeout.connect(self.connect_to_bot)

        self.render_board(chess.Board())
        self.move_bottom_left()
        self.connect_to_bot()

    def connect_to_bot(self):

        if self.socket.state() != QAbstractSocket.SocketState.UnconnectedState:
            return

        self.socket.connectToHost("127.0.0.1", 8001)

        if not self.reconnect_timer.isActive():
            self.reconnect_timer.start()

    def schedule_reconnect(self):

        if not self.reconnect_timer.isActive():
            self.reconnect_timer.start()

    def read_fen_updates(self):

        self.buffer += self.socket.readAll().data()

        while b"\n" in self.buffer:
            raw_fen, self.buffer = self.buffer.split(b"\n", 1)
            fen = raw_fen.decode("utf-8").strip()

            if fen:
                self.render_fen(fen)

    def render_fen(self, fen):

        try:
            board = chess.Board(fen)
        except ValueError:
            return

        self.render_board(board)

    def render_board(self, board):

        svg = chess.svg.board(board, size=240)
        self.board_widget.load(svg.encode("utf-8"))

    def move_bottom_left(self):

        screen = QApplication.primaryScreen()

        if screen is None:
            return

        geometry = screen.availableGeometry()
        self.move(geometry.left(), geometry.bottom() - self.height())


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
