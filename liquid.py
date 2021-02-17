from graphics import *


class Liquid:

    def __init__(self, sx, sy, width, height, color) -> None:
        self.color = color
        self.sx = sx
        self.sy = sy
        self.width = width
        self.height = height
        self.volume = 1
        self.shape = Rectangle(Point(self.sx, self.sy), Point(
            self.sx + self.width, self.sy + (self.height * self.volume)))
        self.shape.setFill(self.color)

    def draw(self, win: GraphWin):
        self.shape.draw(win)

    def undraw(self):
        self.shape.undraw()

    def getColor(self):
        return self.color

    def isColorMatch(self, other_liquid):
        return self.color == other_liquid.getColor()
