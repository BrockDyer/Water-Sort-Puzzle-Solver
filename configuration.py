from tube import Tube
from liquid import Liquid
from graphics import GraphWin


class Configuration:
    def __init__(self, tubes, heuristic=None) -> None:
        self.tubes = tubes
        self.source = None
        self.dest = None
        if heuristic:
            self.heuristic = heuristic
        else:
            self.heuristic = self.calculateHeuristic()

    def _copy(self):
        new_tubes = []
        for tube in self.tubes:
            new_tubes.append(tube.copy())
        return Configuration(new_tubes, self.heuristic)

    def canPour(_, source_tube: Tube, destination_tube: Tube):
        pouring_liquid: Liquid = source_tube.getTopLiquid()
        not_null = pouring_liquid is not None
        pourable = not_null and destination_tube.canAddLiquid(pouring_liquid)
        return pourable

    def _pour(self, source_tube: Tube, destination_tube: Tube, can_pour=False):
        if can_pour or self.canPour(source_tube, destination_tube):
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

    def undraw(self):
        for tube in self.tubes:
            tube.undraw()

    def calculateHeuristic(self):
        calculated_heuristic = 0
        for tube in self.tubes:
            # Unsorted heuristic
            # tube_heuristic = tube.getNumUnsorted()

            # Alternating heuristic
            tube_heuristic = tube.getNumAlternating()
            calculated_heuristic += tube_heuristic

        return calculated_heuristic

    def getChildren(self, debug=False):
        children = set()
        for i in range(len(self.tubes)):
            tube_moves = []
            tube: Tube = self.tubes[i]
            rest = self.tubes[:i] + self.tubes[i+1:]
            for t in rest:
                if self.canPour(tube, t):
                    new_config = self._copy()
                    new_config.source = tube
                    new_config.dest = t

                    # Create child configuration by pouring tube into t
                    tube_idx = int(tube.getName()) - 1
                    t_idx = int(t.getName()) - 1
                    new_config._pour(
                        new_config.tubes[tube_idx], new_config.tubes[t_idx], True)

                    # We need to update the heuristic after the pour
                    new_config.heuristic = new_config.calculateHeuristic()

                    children.add(new_config)

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

    def getHeuristic(self):
        return self.heuristic

    def isGoal(self):
        solved_count = 0
        num_tubes = 0
        for tube in self.tubes:
            if (tube.isSorted() and tube.isFull()) or tube.getNumLiquids() == 0:
                solved_count += 1
            num_tubes += 1

        return solved_count == num_tubes

    def __lt__(self, other: "Configuration"):
        return self.heuristic < other.heuristic

    def __eq__(self, other):
        my_tubes = {}
        for tube in self.tubes:
            tube_str = str(tube)
            if tube_str not in my_tubes:
                my_tubes[tube_str] = 0
            my_tubes[tube_str] += 1

        for tube in other.tubes:
            tube_str = str(tube)
            if tube_str not in my_tubes:
                return False
            my_tubes[tube_str] -= 1
            if my_tubes[tube_str] == 0:
                del my_tubes[tube_str]

        return True

    def __hash__(self):

        result = ""
        for tube in self.tubes:
            tube_str = str(tube)
            result += tube_str

        return hash(result)

    def __str__(self) -> str:
        tubes = []
        for tube in self.tubes:
            tubes.append(str(tube))

        result = "Source: {}\nDestination: {}\n".format(
            self.source.getName() if self.source is not None else None,
            self.dest.getName() if self.dest is not None else None)
        prefix = ""
        for tube in tubes:
            result += prefix + tube
            prefix = '\n'
        return result


if __name__ == "__main__":
    from water_sort import init, create_puzzle, show, get_puzzle_colors, create_tubes

    win = init(500, 400, "Test")
    # tubes = create_puzzle()
    # config = Configuration(tubes)
    # print(config.heuristic())
    # config.draw(win)
    # show(win)
    # children = config.getChildren()
    # print(children[0].heuristic())
    # child = children[0]
    # child.getSource().undraw()
    # child.getDest().undraw()
    # child.draw(win)
    # show(win)

    # win.close()

    # win = init(500, 400, "Test")

    # tubes = []
    # config = Configuration(tubes)
    # print(config.isGoal())

    # tube = Tube("1", 0, 0, 20, 60, 10, 5)
    # tubes = [tube]
    # tube.addLiquid("red")

    # config = Configuration(tubes)
    # print(config.isGoal())

    # config.draw(win)
    # win.getMouse()

    # while not tube.isFull():
    #     tube.addLiquid("red")

    # tube.undraw()
    # print(config.isGoal())
    # config.draw(win)
    # win.getMouse()

    # tubes = create_puzzle()
    # config = Configuration(tubes)
    # config2 = Configuration(tubes)

    # print("{} == {} : {}".format(config, config2, config == config2))

    # config3 = config.getChildren()[0]

    # print("{} == {} : {}".format(config, config3, config == config3))

    # print(config.getHeuristic())

    # config.draw(win)

    # show(win)

    tubes = create_tubes(6)
    tubes2 = create_tubes(6)

    colors = get_puzzle_colors(4)
    colors2 = colors[:]

    for tube in tubes:
        while not (len(colors) == 0) and not tube.isFull():
            tube.addLiquid(colors.pop())

    for tube in tubes2[1:]:
        while not (len(colors2) == 0) and not tube.isFull():
            tube.addLiquid(colors2.pop())

    config = Configuration(tubes)
    config2 = Configuration(tubes2)

    print("{} == {} : {}".format(config, config2, config == config2))
    print("firstHash: {} secondHash: {}".format(hash(config), hash(config2)))

    print("heuristic {}, {}".format(
        config.getHeuristic(), config2.getHeuristic()))

    children = config.getChildren()
    print(len(children))
    best_hscore = min(children)
    print("Parent H: {} Child H: {}".format(
        config.getHeuristic(), best_hscore.getHeuristic()))

    # show(win)
