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


def calculate_heuristic(config: Configuration):
    return config.calculateHeuristic()


def a_star(start: Configuration, h) -> Stack:

    # e_time = 0
    # c_time = 0
    # d_time = 0
    # h_time = 0
    # num_children = 0

    best_delta_h = 0

    frontier = BucketQueue()

    came_from = {start: None}

    g_score = {}
    g_score[start] = 0

    f_score = {}
    f_score[start] = h(start)

    frontier.enqueue(f_score[start], start)

    while not frontier.isEmpty():
        # ts = time.time()
        current = frontier.removeMin()
        # te = time.time()
        # d_time += te - ts

        if current.isGoal():
            # print("Enqueue total time: {}".format(e_time))
            # print("Dequeue total time: {}".format(d_time))
            # print("Heuristic total time: {}".format(h_time))
            # print("Children total time: {} Children average time: {}".format(
            #     c_time, c_time / num_children))

            print("Best delta-h: {}".format(best_delta_h))

            return reconstruct_path(came_from, current)

        # ts = time.time()
        children = current.getChildren()
        # te = time.time()
        # c_time += te - ts

        # num_children += len(children)

        for child in children:
            current_gscore = g_score[current] + \
                1  # cost to next node is just 1
            if child not in g_score or current_gscore < g_score[child]:
                came_from[child] = current
                g_score[child] = current_gscore

                delta_h = h(current) - h(child)
                if delta_h > best_delta_h:
                    best_delta_h = delta_h

                # ts = time.time()
                f_score[child] = g_score[child] + h(child)
                # te = time.time()
                # h_time += te - ts

                # ts = time.time()
                if not frontier.hasValue(child):
                    frontier.enqueue(f_score[child], child)
                # te = time.time()
                # e_time += te - ts

    return Stack()


if __name__ == "__main__":
    from water_sort import create_puzzle, show, init

    tubes = create_puzzle()
    config = Configuration(tubes)
    print(config)

    # win = init(500, 400, "A-Star")
    # config.draw(win)

    # show(win)

    ts = time.time()
    sol = a_star(config, calculate_heuristic)
    te = time.time()

    # print(sol)

    print("Solution found in {}".format(te-ts))
