import sys, random

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QRect

class Tetris(QWidget):
    
    BoardWidth = 10
    BoardHeight = 22
    Coordinates = []

    def __init__(self):
        QWidget.__init__(self)
        self.createCoordinateSystem()
        self.setGeometry(300, 300, 180, 380)
        self.setWindowTitle('Tetris')
        self.center()
        
        self.currPiece = Shape()
        self.currX = 0
        self.currY = 0
        self.insertPiece(self.currPiece)

        self.show()
        

    def center(self):
        screen = self.screen()
        size = self.geometry()
        self.move((screen.size().width() - size.width()) / 2,
        (screen.size().height() - size.height()) / 2)

    def squareHeight(self):
        return self.contentsRect().height() / Tetris.BoardHeight

    def squareWidth(self):
        return self.contentsRect().width() / Tetris.BoardWidth

    def insertPiece(self, shape):
        geom = shape.getGeometry()
        color = shape.getColor()

        y = len(geom)
        x = len(geom[0])
        xpos = random.randint(0, (Tetris.BoardWidth - 1) - x)
        ypos = 0


        self.currX = xpos
        self.currY = ypos

        for i in range(0, y):
            tmp = xpos
            for j in range(0, x):
                if geom[i][j] == 1:
                    Tetris.Coordinates[ypos][tmp] = color
                tmp = tmp + 1
            ypos = ypos + 1

        self.repaint()

    def checkVerticalCollision(self, xpos, ypos):
        geom = self.currPiece.getGeometry()
        y = len(geom)
        lastrow = geom[y - 1]
        lenlastrow = len(lastrow)
        collision = False

        if self.currY == ypos:
            return False
        
        #check if we are at the end of board
        if (ypos > (Tetris.BoardHeight - self.currPiece.getHeight()) ):
            collision = True 
            return collision

        #check if possible new Y position is occupied
        targetpos = ypos - 1 + self.currPiece.getHeight()
        target = Tetris.Coordinates[targetpos]
        index = 0

        for i in range(xpos, xpos + lenlastrow):
            if lastrow[index] == 1 and target[i] != 0:
                collision = True
                break
            index = index + 1

        return collision


    def tryMove(self, xpos, ypos):
        if (xpos < 0) or (xpos > (Tetris.BoardWidth - self.currPiece.getWidth()) ):
            return
        if (ypos < 0): 
            return

        if self.checkVerticalCollision(xpos, ypos):
            self.currPiece = Shape()
            self.insertPiece(self.currPiece)
            return

        geom = self.currPiece.getGeometry()
        color = self.currPiece.getColor()

        y = len(geom)
        x = len(geom[0])

        oldX = self.currX
        oldY = self.currY

        newX = xpos
        newY = ypos

        #clear current position
        for i in range(0, y):
            tmpx = oldX
            for j in range(0, x):
                if geom[i][j] == 1:
                    Tetris.Coordinates[oldY][tmpx] = 0
                tmpx = tmpx + 1
            oldY = oldY + 1
        

        #paint new position
        self.currX = newX
        self.currY = newY

        for i in range(0, y):
            tmpx = newX
            for j in range(0, x):
                if geom[i][j] == 1:
                    Tetris.Coordinates[newY][tmpx] = color
                tmpx = tmpx + 1
            newY = newY + 1 

        self.repaint()


    def drawBackground(self, painter):
        """ just a black background """
        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawRect(0, 0, 180, 380)


    def drawSquare(self, painter, x, y, colorval):
        color = QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        painter.setPen(color)

        painter.setBrush(QColor(colorval))
        painter.drawRect(x * self.squareWidth(), y * self.squareHeight(), self.squareWidth(), self.squareHeight())
                

    def createCoordinateSystem(self):
        """ 22 x 10 array """
        for i in range(Tetris.BoardHeight):
            cols = []
            for j in range(Tetris.BoardWidth):
                cols.append(0)
            Tetris.Coordinates.append(cols)

    
    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBackground(painter)

        #drawPieces
        for i in range(Tetris.BoardHeight):
            for j in range(Tetris.BoardWidth):
                color = Tetris.Coordinates[i][j]
                if color != 0:
                    self.drawSquare(painter, j, i, color)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.tryMove(self.currX - 1 , self.currY)
        elif key == Qt.Key_Right:
            self.tryMove(self.currX + 1, self.currY)
        elif key == Qt.Key_Down:
            self.tryMove(self.currX, self.currY + 1)
        elif key == Qt.Key_Space:
            print("Future work. Move to the end")
        else:
            pass

        event.accept()



class Shape(object):
    LineShape = 1
    SquareShape = 2
    TShape = 3
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    def __init__(self):
        self.currShape = 0
        self.getRandomShape()
        self.width = 0
        self.height = 0

    def getRandomShape(self):
        self.setShape(random.randint(1, 3))

    def setShape(self, shape):
        self.currShape = shape

    def getGeometry(self):
        if self.currShape == Shape.LineShape:
            return self.getLineGeometry()
        if self.currShape == Shape.SquareShape:
            return self.getSquareGeometry()
        if self.currShape == Shape.TShape:
            return self.getTShapeGeometry()

        #default
        return self.getLineGeometry()

    def getLineGeometry(self):
        """ In this case we are returning a line ----"""
        self.setWidth(4)
        self.setHeight(1)
        return [(1, 1, 1, 1)]

    def getSquareGeometry(self):
        """ In this case we are returning a 2x2 square """
        self.setWidth(2)
        self.setHeight(2)
        return [
                (1, 1),
                (1, 1)
                ]

    def getTShapeGeometry(self):
        """ this is an inverted T """
        self.setWidth(3)
        self.setHeight(2)
        return [
                (0, 1, 0),
                (1, 1, 1)
                ]

    def setWidth(self, w):
        self.width = w

    def setHeight(self, h):
        self.height = h

    def getWidth(self):
        return self.width 

    def getHeight(self):
        return self.height

    def getColor(self):
        return Shape.colorTable[self.currShape]




app = QApplication(sys.argv)
tetris = Tetris()
tetris.show()
sys.exit(app.exec())