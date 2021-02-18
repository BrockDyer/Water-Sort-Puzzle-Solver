from tube import Tube
from liquid import Liquid
from graphics import GraphWin


class Configuration:
    def __init__(self, tubes) -> None:
        self.tubes = tubes
        self.source = None
        self.dest = None
        self.parent = None
        self.depth = 0
        self.heuristic = self.calculateHeuristic()

    def _copy(self):
        new_tubes = []
        for tube in self.tubes:
            new_tubes.append(tube.copy())
        return Configuration(new_tubes)

    def canPour(_, source_tube: Tube, destination_tube: Tube):
        pouring_liquid: Liquid = source_tube.getTopLiquid()
        not_null = pouring_liquid is not None
        pourable = not_null and destination_tube.canAddLiquid(pouring_liquid)
        return pourable

    def _pour(self, source_tube: Tube, destination_tube: Tube):
        if self.canPour(source_tube, destination_tube):
            pour_liquid: Liquid = source_tube.removeLiquid()
            destination_tube.addLiquid(pour_liquid.getColor())
            try:
                self._pour(source_tube, destination_tube)
            except(ValueError):
                pass
        else:
            raise ValueError("Cannot pour tube: {} into tube:{}".format(
                source_tube.getName(), destination_tube.getName()))

    def pour(self, idx1, idx2, win: GraphWin):
        source: Tube = self.tubes[idx1]
        dest: Tube = self.tubes[idx2]

        source.undraw()
        dest.undraw()

        msg = "Poured tube #{} into tube #{}".format(idx1 + 1, idx2 + 1)

        try:
            self._pour(source, dest)
        except(ValueError):
            msg = "Cannot pour tube #{} into tube #{}".format(
                idx1 + 1, idx2 + 1)

        source.draw(win)
        dest.draw(win)

        return msg

    def draw(self, win: GraphWin):
        for tube in self.tubes:
            tube.draw(win)

    def calculateHeuristic(self):
        min_moves_left = 0
        for tube in self.tubes:
            min_moves_left += tube.getNumUnsorted()

        return min_moves_left

    def getChildren(self, debug=False):
        children = []
        for i in range(len(self.tubes)):
            tube_moves = []
            tube: Tube = self.tubes[i]
            rest = self.tubes[:i] + self.tubes[i+1:]
            for t in rest:
                if self.canPour(tube, t):
                    new_config = self._copy()
                    new_config.source = tube
                    new_config.dest = t
                    new_config.parent = self
                    new_config.depth = self.depth + 1
                    new_config.heuristic = self.calculateHeuristic()
                    tube_idx = int(tube.getName()) - 1
                    t_idx = int(t.getName()) - 1
                    new_config._pour(
                        new_config.tubes[tube_idx], new_config.tubes[t_idx])
                    children.append(new_config)
                    if debug:
                        tube_moves.append(
                            "#{} -> #{}".format(tube.getName(), t.getName()))
            if debug:
                print(tube_moves)

        return children

    def getSource(self):
        return self.source

    def getDest(self):
        return self.dest

    def getParent(self):
        return self.parent

    def hScore(self):
        return self.heuristic

    def gScore(self):
        return self.depth

    def fScore(self):
        return self.depth + self.heuristic

    def isGoal(self):
        solved_count = 0
        num_tubes = 0
        for tube in self.tubes:
            if (tube.isSorted() and tube.isFull()) or tube.getNumLiquids() == 0:
                solved_count += 1
            num_tubes += 1

        return solved_count == num_tubes

    def __lt__(self, other):
        return self.fScore() < other.fScore()


if __name__ == "__main__":
    from water_sort import init, create_puzzle, show

    win = init(500, 400, "Test")
    tubes = create_puzzle()
    config = Configuration(tubes)
    print(config.heuristic())
    config.draw(win)
    show(win)
    children = config.getChildren()
    print(children[0].heuristic())
    child = children[0]
    child.getSource().undraw()
    child.getDest().undraw()
    child.draw(win)
    show(win)

    win.close()

    win = init(500, 400, "Test")

    tubes = []
    config = Configuration(tubes)
    print(config.isGoal())

    tube = Tube("1", 0, 0, 20, 60, 10, 5)
    tubes = [tube]
    tube.addLiquid("red")

    config = Configuration(tubes)
    print(config.isGoal())

    config.draw(win)
    win.getMouse()

    while not tube.isFull():
        tube.addLiquid("red")

    tube.undraw()
    print(config.isGoal())
    config.draw(win)
    win.getMouse()
