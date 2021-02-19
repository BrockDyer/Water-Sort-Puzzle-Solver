from graphics import *
from util.stack import Stack
from liquid import Liquid


class Tube:

    def __init__(self, name, sx, sy, width, height, height_per_volume, liquid_capacity) -> None:
        self.name = name
        self.sx = sx
        self.sy = sy
        self.width = width
        self.height = height
        self.height_per_volume = height_per_volume
        self.capacity = liquid_capacity
        self.liquids = Stack()
        self.colors = {}

    def draw(self, win: GraphWin):

        Text(Point(self.sx + (self.width // 2),
                   self.sy + (self.width // 2)), self.name).draw(win)

        Line(Point(self.sx, self.sy), Point(
            self.sx, self.sy - self.height)).draw(win)
        Line(Point(self.sx + self.width, self.sy), Point(self.sx +
                                                         self.width, self.sy - self.height)).draw(win)
        Line(Point(self.sx, self.sy - self.height),
             Point(self.sx + self.width, self.sy - self.height)).draw(win)

        tmp_liquids = Stack()
        while not self.liquids.isEmpty():
            liquid: Liquid = self.liquids.pop()
            liquid.draw(win)
            tmp_liquids.push(liquid)

        self.liquids = tmp_liquids.reverse()

    def undraw(self):
        tmp_liquids = Stack()
        while not self.liquids.isEmpty():
            liquid: Liquid = self.liquids.pop()
            liquid.undraw()
            tmp_liquids.push(liquid)

        self.liquids = tmp_liquids.reverse()

    def getNumLiquids(self):
        return self.liquids.getSize()

    def getName(self):
        return self.name

    def getTopLiquid(self):
        if self.liquids.isEmpty():
            return None
        return self.liquids.top()

    def isFull(self):
        return self.getNumLiquids() == self.capacity

    def canAddLiquid(self, liquid):
        liquids_match = self.liquids.isEmpty() or self.liquids.top().isColorMatch(liquid)
        has_room = not self.isFull()
        return liquids_match and has_room

    def addLiquid(self, color):
        sx = self.sx
        sy = self.sy - self.height + \
            self.height_per_volume * (self.getNumLiquids())
        liquid = Liquid(sx, sy, self.width, self.height_per_volume, color)
        self.liquids.push(liquid)

        if color not in self.colors:
            self.colors[color] = 0

        self.colors[color] += 1

    def removeLiquid(self):
        if not self.liquids.isEmpty():
            liquid = self.liquids.pop()
            self.colors[liquid.getColor()] -= 1
            return liquid

    def copy(self):
        tmp = Stack()
        while not self.liquids.isEmpty():
            liquid: Liquid = self.liquids.pop()
            tmp.push(liquid)

        new_tube = Tube(self.name, self.sx, self.sy, self.width,
                        self.height, self.height_per_volume, self.capacity)

        while not tmp.isEmpty():
            liquid: Liquid = tmp.pop()
            new_tube.addLiquid(liquid.getColor())
            self.liquids.push(liquid)

        return new_tube

    def isSorted(self):
        still_has = set(c for c in self.colors if self.colors[c] > 0)
        return len(still_has) == 1

    def getNumUnsorted(self):
        still_has = set(c for c in self.colors if self.colors[c] > 0)
        result = len(still_has)
        return result if result > 0 else 0

    def getNumAlternating(self):
        alt = 0
        tmp = Stack()
        prev_color = None
        while not self.liquids.isEmpty():
            liquid = self.liquids.pop()
            color = liquid.getColor()
            if not color == prev_color and prev_color is not None:
                alt += 1
            prev_color = color
            tmp.push(liquid)

        self.liquids = tmp.reverse()
        return alt

    def __str__(self) -> str:
        tmp = Stack()
        result = ""
        while not self.liquids.isEmpty():
            liquid = self.liquids.pop()
            result += liquid.getColor() + " -> "
            tmp.push(liquid)

        self.liquids = tmp.reverse()
        return result


if __name__ == "__main__":
    test_tube = Tube("Test", 0, 0, 20, 60, 10, 5)
    test_tube.addLiquid('blue')
    # test_tube.addLiquid('blue')
    test_tube.addLiquid('blue')
    test_tube.addLiquid('red')

    width = 500
    height = 400
    win = GraphWin("test", width, height)
    win.setCoords(-width / 2, -height / 2, width / 2, height / 2)
    test_tube.draw(win)

    print(test_tube.getNumUnsorted())
    print("Contiguous: {}".format(test_tube.getNumContiguous()))

    win.getMouse()

    new_tube = test_tube.copy()
    print(test_tube)

    test_tube.undraw()
    win.getMouse()
    new_tube.removeLiquid()
    new_tube.draw(win)
    print(new_tube)
    print(new_tube.getNumUnsorted())

    win.getMouse()
