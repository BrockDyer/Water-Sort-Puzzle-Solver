from graphics import *


class Arc(Oval):
    """
    An extension to Zelle graphics module to draw a semi-circle.
    Written by StackOverflow user cdlane
    https://stackoverflow.com/questions/27263091/how-can-i-make-a-semi-circle-using-zelle-graphics-in-python
    """

    def __init__(self, p1, p2, extent):
        self.extent = extent
        super().__init__(p1, p2)

    def __repr__(self):
        return "Arc({}, {}, {})".format(str(self.p1), str(self.p2), self.extent)

    def clone(self):
        other = Arc(self.p1, self.p2, self.extent)
        other.config = self.config.copy()
        return other

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        options['style'] = tk.CHORD
        options['extent'] = self.extent
        return canvas.create_arc(x1, y1, x2, y2, options)
