from Queens import Square, Piece, Board, Game
import Solutions
import sys
import os

try:
    from PyQt6 import QtGui, QtWidgets, QtCore
    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
except ImportError:
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtCore import Signal, Slot

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


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, width, height, color):
        super(ClickableLabel, self).__init__()
        pixmap = QtGui.QPixmap(width, height)
        pixmap.fill(QtGui.QColor(color))
        self.setPixmap(pixmap)
        self.setObjectName(color)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


# class QTClickableQueen(QtWidgets.Qlabel):
#     clicked = QtCore.pyqtSignal(str)

#     def __init__(self:
#         super().__init__()


class QTQueen(Piece,QtWidgets.QLabel):
    def __init__(self,type,file,rank,board):
        Piece.__init__(self,type,file,rank,board)
        QtWidgets.QLabel.__init__(self)
        self.image = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitequeen.png'))
        self.setMinimumSize(32, 32)
        self.initUI()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0 + size // 4, 0 + size // 4, self.image.scaled(
            size // 2, size // 2, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

    def initUI(self):

        self.setAcceptDrops(True)
        # self.button = Button('Button', self)
        # self.button.move(100, 65)

        # self.setWindowTitle('Click or Move')
        # self.setGeometry(300, 300, 550, 450)


    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        position = e.position()
        self.image.move(position.toPoint())

        e.setDropAction(QtCore.Qt.DropAction.MoveAction)
        e.accept()
        

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


class ChessGame(Game,QtWidgets.QMainWindow):
    def __init__(self):
        Game.__init__(self)
        QtWidgets.QMainWindow.__init__(self)
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        self.board = QTBoard()
        layout.addWidget(self.board)
        # self.table = QtWidgets.QTableWidget(1, 3)
        # layout.addWidget(self.table)
        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18))
        quit.clicked.connect(QtWidgets.QApplication.quit)
        layout.addWidget(quit)



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


class Button(QtWidgets.QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.MouseButton.RightButton:
            return

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        drag.setHotSpot(e.position().toPoint() - self.rect().topLeft())

        dropAction = drag.exec(QtCore.Qt.DropAction.MoveAction)


    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            print('press')


def main():
    app = QtWidgets.QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec())

main()
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
