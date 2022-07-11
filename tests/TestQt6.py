from PyQt6 import QtCore, QtGui, QtWidgets
import os

class Square(QtWidgets.QWidget):
    def __init__(self,type):
        super().__init__()
        self.type = type
        self.piece = None
        self.image = self.classify()
        self.setMinimumSize(32, 32)

    def classify(self):
        if self.type == 0:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitesquare.png'))
        elif self.type == 1:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'blacksquare.png'))

    def has_piece(self):
        return False

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

class Queen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.image = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitequeen.png'))
        self.setMinimumSize(32, 32)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))


class Board(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # self.background = QtGui.QPixmap('chessboard.png')

        for row in range(8):
            layout.setRowStretch(row, 1)
            layout.setColumnStretch(row, 1)
            for col in range(8):
                if col % 2 == 0 and row % 2 == 0:
                    layout.addWidget(Square(0), row, col)
                elif col % 2 == 1 and row % 2 == 1:
                    layout.addWidget(Square(0), row, col)
                elif col % 2 == 1 and row % 2 == 0:
                    layout.addWidget(Square(1), row, col)
                elif col % 2 == 0 and row % 2 == 1:
                    layout.addWidget(Square(1), row, col)

                #add queens along diag
        # for row in range(8):
            layout.addWidget(Queen(), row, 0)


    def minimumSizeHint(self):
        return QtCore.QSize(256, 256)

    def sizesHint(self):
        return QtCore.QSize(768, 768)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        rect = QtCore.QRect(0, 0, size, size)
        rect.moveCenter(self.rect().center())
        self.layout().setGeometry(rect)

    # def paintEvent(self, event):
    #     qp = QtGui.QPainter(self)
    #     rect = self.layout().geometry()
    #     qp.drawPixmap(rect, self.background.scaled(rect.size(), 
    #         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class ChessGame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        self.board = Board()
        layout.addWidget(self.board)
        self.table = QtWidgets.QTableWidget(1, 3)
        layout.addWidget(self.table)


import sys
import os
print(sys.path)
script_dir = os.path.dirname(__file__)
print(os.path.join(os.path.dirname(__file__), '..', 'images', 'blacksquare.png'))
app = QtWidgets.QApplication(sys.argv)
game = ChessGame()
game.show()
sys.exit(app.exec())