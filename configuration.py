from water_sort import LIQUID_PER_TUBE, LIQUID_UNIT_VOLUME
from tube import Tube
from liquid import Liquid
from graphics import GraphWin


class Configuration:
    def __init__(self, tubes) -> None:
        self.tubes = tubes

    def _copy(self):
        return Configuration(self.tubes[:])

    def canPour(_, source_tube: Tube, destination_tube: Tube):
        pouring_liquid: Liquid = source_tube.getTopLiquid()
        not_null = pouring_liquid is not None
        pourable = destination_tube.canAddLiquid(pouring_liquid)
        return not_null and pourable

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


if __name__ == "__main__":
    from water_sort import init, create_puzzle, show

    win = init(500, 400, "Test")
    tubes = create_puzzle()
    config = Configuration(tubes)
    config.draw(win)
    show(win)

    show(win)
