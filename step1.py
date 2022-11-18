import sys, random

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Qt

class Tetris(QWidget):

    BoardWidth = 10
    BoardHeight = 22
    Coordinates = []

    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(300, 300, 180, 380)
        self.createCoordinateSystem()
        self.setWindowTitle('Tetris')
        self.center()

        self.show()

    def center(self):
        screen = self.screen()
        size = self.geometry()
        self.move((screen.size().width() - size.width()) / 2,
        (screen.size().height() - size.height()) / 2)
    
    def createCoordinateSystem(self):
        for i in range(Tetris.BoardHeight):
            cols = []
            for j in range(Tetris.BoardWidth):
                cols.append(0)
            Tetris.Coordinates.append(cols)

        Tetris.Coordinates[0][0] = 1
        Tetris.Coordinates[0][1] = 1
        Tetris.Coordinates[1][0] = 1
        Tetris.Coordinates[1][1] = 1
    
    def squareHeight(self):
        return self.contentsRect().height() / Tetris.BoardHeight
    
    def squareWidth(self):
        return self.contentsRect().width() / Tetris.BoardWidth
    
    def drawBackground(self, painter):
        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawRect(0, 0, 180, 380)
    
    def drawSquare(self, painter, x, y):
        color = QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        painter.setPen(color)

        painter.setBrush(QColor('#DAAA00'))
        painter.drawRect(x, y, self.squareWidth(), self.squareHeight())
    

    def moveLeft(self):
        for i in range(Tetris.BoardHeight):
            for j in range(Tetris.BoardWidth):
                if Tetris.Coordinates[i][j] == 1:
                    if (j > 0):
                        Tetris.Coordinates[i][j-1] = 1
                        Tetris.Coordinates[i][j] = 0
        
        self.repaint()

    def moveRight(self):
        for i in range(Tetris.BoardHeight):
            for j in reversed(range(Tetris.BoardWidth)):
                if Tetris.Coordinates[i][j] == 1:
                    if (j + 1 < Tetris.BoardWidth):
                        Tetris.Coordinates[i][j+1] = 1
                        Tetris.Coordinates[i][j] = 0

        self.repaint() 

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBackground(painter)

        #self.drawSquare(painter, 0, 0) #coordinate (x, y) 0,0 
        for i in range(Tetris.BoardWidth):
            for j in range(Tetris.BoardHeight):
                if Tetris.Coordinates[j][i] == 1:
                    self.drawSquare(painter, i * self.squareWidth(), j * self.squareHeight())

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            print("moving to the left")
            self.moveLeft()

        if key == Qt.Key_Right:
            print("moving to the right")
            self.moveRight()
        event.accept()



#entrypoint
app = QApplication(sys.argv)
tetris = Tetris()
tetris.show()
sys.exit(app.exec())
     

