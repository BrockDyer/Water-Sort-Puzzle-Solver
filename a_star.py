from util.bucket_queue import BucketQueue
from configuration import Configuration
from util.bucket_queue import BucketQueue
from configuration import Configuration
from util.stack import Stack
import time


def reconstruct_path(came_from: dict, current: Configuration) -> Stack:
    path = Stack()
    while current is not None:
        path.push(current)
        current = came_from[current]

    return path


def a_star(start: Configuration) -> Stack:
    frontier = BucketQueue(100)

    came_from = {start: None}

    g_score = {}
    g_score[start] = 0

    f_score = {}
    f_score[start] = start.getHeuristic()

    frontier.enqueue(f_score[start], start)

    while not frontier.isEmpty():
        current = frontier.removeMin()
        if current.isGoal():
            return reconstruct_path(came_from, current)

        children = current.getChildren()
        for child in children:
            current_gscore = g_score[current] + \
                1  # cost to next node is just 1
            if child not in g_score or current_gscore < g_score[child]:
                came_from[child] = current
                g_score[child] = current_gscore
                f_score[child] = g_score[child] + child.getHeuristic()

                if not frontier.hasValue(child):
                    frontier.enqueue(f_score[child], child)

    return Stack()


if __name__ == "__main__":
    from water_sort import create_puzzle

    tubes = create_puzzle()
    config = Configuration(tubes)
    print(config)

    ts = time.time()
    sol = a_star(config)
    te = time.time()

    print(sol)

    print("Solution found in {}".format(te-ts))
