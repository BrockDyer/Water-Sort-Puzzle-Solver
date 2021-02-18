from configuration import Configuration
from util.priority_queue import PriorityQueue
from configuration import Configuration
from util.stack import Stack


def reconstruct_path(came_from: dict, current: Configuration) -> Stack:
    path = Stack()
    while current is not None:
        path.push(current)
        current = came_from[current]

    return path


def a_star(start: Configuration) -> Stack:
    frontier = PriorityQueue()

    came_from = {start: None}

    g_score = {}
    g_score[start] = 0

    f_score = {}
    f_score[start] = start.getHeuristic()

    frontier.enqueue((f_score[start], start))

    while not frontier.isEmpty():
        _, current = frontier.dequeue()
        if current.isGoal():
            print("Found goal: {}".format(current))
            return reconstruct_path(came_from, current)

        children = current.getChildren()
        for child in children:
            current_gscore = g_score[current] + \
                1  # cost to next node is just 1
            if child not in g_score or current_gscore < g_score[child]:
                came_from[child] = current
                g_score[child] = current_gscore
                f_score[child] = g_score[child] + child.getHeuristic()
                frontier.enqueue((f_score[child], child))

    return Stack()


if __name__ == "__main__":
    from water_sort import create_puzzle

    tubes = create_puzzle()
    config = Configuration(tubes)
    print(config)

    sol = a_star(config)

    print(sol)
