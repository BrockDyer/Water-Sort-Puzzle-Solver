from tube import Tube
from liquid import Liquid
from graphics import GraphWin


class Configuration:
    def __init__(self, tubes) -> None:
        self.tubes = tubes
        self.source = None
        self.dest = None

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


if __name__ == "__main__":
    from water_sort import init, create_puzzle, show

    win = init(500, 400, "Test")
    tubes = create_puzzle()
    config = Configuration(tubes)
    config.draw(win)
    show(win)
    children = config.getChildren()
    show(win)
    selected = children[0]
    selected.getSource().undraw()
    selected.getDest().undraw()
    selected.draw(win)
    show(win)
