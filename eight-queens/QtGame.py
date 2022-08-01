from Queens import Square, Piece, Board, Game
import Solutions
import sys
import os

PREFERRED_GUI_IMPLEMENTATION = "PyQt6"

if PREFERRED_GUI_IMPLEMENTATION == "PyQt6":
    try:
        from PyQt6 import QtGui, QtWidgets, QtCore
        from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    except ImportError:
        from PySide6 import QtGui, QtWidgets, QtCore
        from PySide6.QtCore import Signal, Slot
elif PREFERRED_GUI_IMPLEMENTATION == "PySide6":
    try:
        from PySide6 import QtGui, QtWidgets, QtCore
        from PySide6.QtCore import Signal, Slot
    except ImportError:
        from PyQt6 import QtGui, QtWidgets, QtCore
        from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

class ChessBoard(Board,QtWidgets.QWidget):
    def __init__(self):
        Board.__init__(self,8)
        self.initUI()

    def initUI(self):
        QtWidgets.QWidget.__init__(self)

        ##Setup layout of qt widgets
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        #event handling for moves
        self.setAcceptDrops(True)           

        ##Construct the board
        for row in range(self.b_dim):
            layout.setRowStretch(row, 1)
            layout.setColumnStretch(row, 1)
            for col in range(self.b_dim):
                if col % 2 == 0 and row % 2 == 0:
                    layout.addWidget(ChessSquare(self,row,col,0), row, col)
                elif col % 2 == 1 and row % 2 == 1:
                    layout.addWidget(ChessSquare(self,row,col,0), row, col)
                elif col % 2 == 1 and row % 2 == 0:
                    layout.addWidget(ChessSquare(self,row,col,1), row, col)
                elif col % 2 == 0 and row % 2 == 1:
                    layout.addWidget(ChessSquare(self,row,col,1), row, col)

        # add some pieces to the puzzle board
        for rank in range(self.b_dim):
            layout.addWidget(ChessPiece("Qu",rank,rank,self), rank, rank)

    #Painting and Sizing
    def minimumSizeHint(self):
        return QtCore.QSize(256, 256)

    def sizesHint(self):
        return QtCore.QSize(768, 768)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        rect = QtCore.QRect(0, 0, size, size)
        rect.moveCenter(self.rect().center())
        self.layout().setGeometry(rect)
    
    #Mouse Event Handling
    def dragEnterEvent(self, e):
        e.accept()

    def listchildWidgets(self):
        #print the square and pieces
        print(self.findChildren(QtWidgets.QWidget))
        #print the pieces
        #print(self.findChildren(QtWidgets.QLabel))

    def listChildWidget(self):
        print(self.findChild(QtWidgets.QWidget))

    def listLayoutChildWidgets(self):
        # print(self.layout.findChild(QWidget))
        for i in range(self.layout.count()):
            print(self.layout.itemAt(i).widget().text())        
    def mousePressEvent(self, event):
        self.listchildWidgets()
        # self.listLayoutChildWidgets()
        # self.listChildWidget()
        return
        piece = self.childAt(event.pos())
        del piece
        if (event.button() == QtCore.Qt.MouseButton.LeftButton
              # and event.pos() 
            # and iconLabel.geometry().contains(event.pos())
            ):
            if self.childAt(event.pos()).has_piece():
                drag = QtGui.QDrag(self)
                mimeData = QtCore.QMimeData()
                mimeData.setImageData(QtGui.QImage(self.childAt(event.pos()).image_dest))
                drag.setMimeData(mimeData)
                drag.setPixmap(self.childAt(event.pos()).image)
                dropAction = drag.exec()
        elif (event.button() == QtCore.Qt.MouseButton.RightButton):
            print(event.pos())    

class ChessSquare(Square,QtWidgets.QWidget):
    def __init__(self,board,rank,file,color):
        Square.__init__(self,board,rank,file)
        self.color = color
        self.image = self.set_image()
        # self.image = self.initUI()
        self.initUI()
        
    def initUI(self):
        QtWidgets.QWidget.__init__(self)
        self.setMinimumSize(32, 32)

    def set_image(self):
        if self.color == 0:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitesquare.png'))
        elif self.color == 1:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'blacksquare.png'))
        elif self.color == 2:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'whitesquare-selected.png'))
        elif self.color == 3:
            return QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '..', 'images', 'blacksquare-selected.png'))
        

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

    # def __str__(self):
    #     return str(self.get_piece_type()) + '@' + ''.join(map(str,(chr(ord('A') + (Square.fetch_board(self).b_size - 1) - self.location[0]),Square.fetch_board(self).b_size - self.location[1])))

    # def __repr__(self):
        # return str(self.piece_type) + '@' + ''.join(map(str,(chr(ord('A') + (self.fetch_board(self).b_size - 1) - self.location[0]),self.fetch_board(self).b_size - self.location[1])))

    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.MouseButton.LeftButton:
    #         self.type = (self.type + 2) % 4
    #         self.image = self.classify()
    #         self.update()
    #     else:
    #         return QtWidgets.QWidget.mousePressEvent(self,event)

# class ClickableLabel(QtWidgets.QLabel):
#     # clicked = QtCore.pyqtSignal(str)

#     def __init__(self, width, height, color):
#         super(ClickableLabel, self).__init__()
#         pixmap = QtGui.QPixmap(width, height)
#         pixmap.fill(QtGui.QColor(color))
#         self.setPixmap(pixmap)
#         self.setObjectName(color)

#     def mousePressEvent(self, event):
#         self.clicked.emit(self.objectName())


# class QTClickableQueen(QtWidgets.Qlabel):
#     clicked = QtCore.pyqtSignal(str)

#     def __init__(self:
#         super().__init__()


class ChessPiece(Piece,QtWidgets.QLabel):
    def __init__(self,type,file,rank,board):
        Piece.__init__(self,type,file,rank,board)
        self.image_dest = os.path.join(os.path.dirname(__file__), '..', 'images', 'whitequeen.png')
        self.initUI()
    
    def initUI(self):
        QtWidgets.QLabel.__init__(self)
        self.image = QtGui.QPixmap(self.image_dest)
        self.setMinimumSize(32, 32)
        # self.setAcceptDrops(True)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0 + size // 4, 0 + size // 4, self.image.scaled(
            size // 2, size // 2, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

    # def mousePressEvent(self, event):
        # if (event.button() == QtCore.Qt.MouseButton.LeftButton
              # # and event.pos() 
            # # and iconLabel.geometry().contains(event.pos())
            # ):
            # drag = QtGui.QDrag(self)
            # mimeData = QtCore.QMimeData()
            # mimeData.setImageData(QtGui.QImage(self.image_dest))
            # drag.setMimeData(mimeData)
            # drag.setPixmap(self.image)
            # dropAction = drag.exec()
        # elif (event.button() == QtCore.Qt.MouseButton.RightButton):
            # print(event.pos())

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        
        self.get_square().set_piece("Qu")
        # position = e.position()
        # self.image.move(position.toPoint())
        e.setDropAction(QtCore.Qt.DropAction.MoveAction)
        e.accept()        



    # def paintEvent(self, event):
    #     qp = QtGui.QPainter(self)
    #     rect = self.layout().geometry()
    #     qp.drawPixmap(rect, self.background.scaled(rect.size(), 
    #         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class ChessGame(Game,QtWidgets.QMainWindow):
    def __init__(self):
        Game.__init__(self)
        self.board = ChessBoard()
        self.initUI()

    def initUI(self):
        QtWidgets.QMainWindow.__init__(self)
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec())

main()