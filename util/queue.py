from .node import Node


class Queue:

    def __init__(self) -> None:
        self.front = None
        self.back = None
        self.size = 0

    def isEmpty(self):
        return self.front is None

    def getSize(self):
        return self.size

    def enqueue(self, value):
        node = Node(value)
        if self.isEmpty():
            self.front = node
        else:
            self.back.setNext(node)

        self.back = node
        self.size += 1

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Tried to dequeue from empty queue")
        front = self.front.getValue()
        self.front = self.front.getNext()
        if self.isEmpty():
            self.back = None

        return front


if __name__ == "__main__":
    from random import randint
    queue = Queue()
    for i in range(10):
        queue.enqueue(i)

    while not queue.isEmpty():
        print(queue.dequeue())
        r = randint(0, 4)
        if r == 1:
            r = randint(10, 15)
            queue.enqueue(r)
            print("Added {} to the queue".format(r))
