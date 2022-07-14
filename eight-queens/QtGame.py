from Queens import Square, Queen, Board
import Solutions
import sys
import os

try:
    from PyQt6 import QtGui, QtWidgets, QtCore
    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
except ImportError:
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtCore import Signal, Slot

#if 'PyQt6' in sys.modules:
#   # PyQt6
#    from PyQt6 import QtGui, QtWidgets, QtCore
#    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
#
#
#else:
#    # PySide6
#    from PySide6 import QtGui, QtWidgets, QtCore
#    from PySide6.QtCore import Signal, Slot

class QTSquare(Square,QtWidgets.QWidget):
    def __init__(self,board,file,rank,color):
        Square.__init__(self,board,file,rank)
        QtWidgets.QWidget.__init__(self)
        self.type = color
        self.piece = None
        self.image = self.classify()
        self.setMinimumSize(32, 32)

    def classify(self):
        if self.type == 0:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitesquare.png'))
        elif self.type == 1:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'blacksquare.png'))

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

class QTQueen(Queen,QtWidgets.QWidget):
    def __init__(self,type,file,rank,board):
        Queen.__init__(self,type,file,rank,board)
        QtWidgets.QWidget.__init__(self)
        self.image = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitequeen.png'))
        self.setMinimumSize(32, 32)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size // 2, size // 2, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))


class QTBoard(Board,QtWidgets.QWidget):
    def __init__(self):
        Board.__init__(self,8)
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # self.background = QtGui.QPixmap('chessboard.png')

        for row in range(8):
            layout.setRowStretch(row, 1)
            layout.setColumnStretch(row, 1)
            for col in range(8):
                if col % 2 == 0 and row % 2 == 0:
                    layout.addWidget(QTSquare(self,col,row,0), row, col)
                elif col % 2 == 1 and row % 2 == 1:
                    layout.addWidget(QTSquare(self,col,row,0), row, col)
                elif col % 2 == 1 and row % 2 == 0:
                    layout.addWidget(QTSquare(self,col,row,1), row, col)
                elif col % 2 == 0 and row % 2 == 1:
                    layout.addWidget(QTSquare(self,col,row,1), row, col)

                #add queens along diag
        # for row in range(8):
            layout.addWidget(QTQueen("Qu",col,row,self), row, 0)


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
        self.board = QTBoard()
        layout.addWidget(self.board)
        self.table = QtWidgets.QTableWidget(1, 3)
        layout.addWidget(self.table)


def _enum(obj, name):
    parent, child = name.split('.')
    result = getattr(obj, child, False)
    if result:  # Found using short name only.
        return result

    obj = getattr(obj, parent)  # Get parent, then child.
    return getattr(obj, child)


def _exec(obj):
    if hasattr(obj, 'exec'):
        return obj.exec()
    else:
        return obj.exec_()


def main(self):
    app = QtWidgets.QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec())

#  #Testing#  Solution Algorithms #
    # for game in games:
        # if MODE_GAME == 1:
            # if DEBUG:
                # print("Solving...")
            # Solutions.solveNQ(games[uuid])
            # print(g)

        # elif MODE_GAME == 2:
            # Board.setup_queens(games[uuid])
      


        #Print the empty boards
        # print(g.fetch_board(uuid))
        #test move a piece
        # g.fetch_board(uuid).brd[0][0].move_piece(1,1)

        #Solve them
        # Solutions.solveNQ(g.fetch_board(uuid).brd)

# 
