from configuration import Configuration
from graphics import *
from tube import Tube
from configuration import Configuration
from a_star import a_star, calculate_heuristic
from random import randint, shuffle


WINDOW_WIDTH = 500
WINDOW_HEIGHT = WINDOW_WIDTH * 4 // 5
WINDOW_NAME = "Water Sort Puzzle"

TUBE_HEIGHT = 60
TUBE_WIDTH = TUBE_HEIGHT // 3
TUBE_VOLUME = TUBE_HEIGHT * 5 // 6
LIQUID_PER_TUBE = 4
LIQUID_UNIT_VOLUME = TUBE_VOLUME // LIQUID_PER_TUBE

NUMBER_OF_TUBES = 8
EMPTY_TUBES = 2

COLORS = ["red", "blue", "green", "purple",
          "yellow", "orange", "pink", "cyan", "gray", "lime", "magenta", "dark red", "green yellow", "navy"]


def init(width, height, window_name):
    win = GraphWin(window_name, width, height)
    win.setCoords(-width / 2, -height / 2, width / 2, height / 2)
    return win


def create_tubes(n):

    tubes = []

    row_width = TUBE_WIDTH * (n / 2) + TUBE_WIDTH * ((n / 2) - 1)
    row_space = TUBE_WIDTH  # space between each tube
    col_space = TUBE_WIDTH * 2  # space between each row

    sx = 0 - (row_width // 2)
    sxv = sx
    sy = 0 + col_space // 2 + TUBE_HEIGHT

    for i in range(n):
        if i == (n // 2):
            sy -= TUBE_HEIGHT + col_space
            sxv = sx

        tubes.append(Tube(str(i+1), sxv, sy, TUBE_WIDTH,
                          TUBE_HEIGHT, LIQUID_UNIT_VOLUME, LIQUID_PER_TUBE))
        sxv += TUBE_WIDTH + row_space

    return tubes


def show(win: GraphWin):
    win.getMouse()


def get_puzzle_colors(n):
    colors = set()
    while len(colors) < n:
        colors.add(COLORS[randint(0, len(COLORS) - 1)])

    result = []
    for color in colors:
        for _ in range(LIQUID_PER_TUBE):
            result.append(color)

    shuffle(result)
    return result


def create_puzzle():
    tubes = create_tubes(NUMBER_OF_TUBES)
    colors = get_puzzle_colors(NUMBER_OF_TUBES - EMPTY_TUBES)

    for tube in tubes:
        while not (len(colors) == 0) and not tube.isFull():
            tube.addLiquid(colors.pop())

    return tubes


def display_text(text, win: GraphWin, display=None):
    loc = Point(0, 0 - TUBE_HEIGHT - (TUBE_WIDTH * 2))
    if display:
        display.undraw()
    display = Text(loc, text)
    display.draw(win)
    return display


def main():
    tubes = create_puzzle()
    win = init(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME)
    start_config = Configuration(tubes)
    start_config.draw(win)

    display = display_text("Click to solve", win)

    # print(start_config.getHeuristic())

    show(win)

    start_config.undraw()
    display = display_text("Solving...", win, display)

    ts = time.time()
    sol = a_star(start_config, calculate_heuristic)
    te = time.time()

    # print(sol)

    print("Solution found in {}".format(te-ts))

    tmp = sol.pop()
    while tmp is not None:

        tmp.draw(win)
        next_config = sol.pop() if not sol.isEmpty() else None
        display = display_text(
            "#{} -> #{}; Click to continue".format(
                next_config.getSource().getName(), next_config.getDest().getName()
            ) if next_config else "Solved",
            win, display)

        show(win)

        tmp.undraw()
        tmp = next_config


if __name__ == "__main__":
    main()
