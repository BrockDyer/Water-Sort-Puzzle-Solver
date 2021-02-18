from .node import Node


class PriorityQueue:

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
            self.back = node
        else:
            if self.front.getValue() > node.getValue():
                after = self.front
                node.setNext(after)
                self.front = node
            else:
                tmp = self.front
                while tmp.getNext() is not None and tmp.getNext().getValue() < node.getValue():
                    tmp = tmp.getNext()

                after = tmp.getNext()
                tmp.setNext(node)
                node.setNext(after)

        self.size += 1

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Tried to dequeue from empty queue")
        front = self.front.getValue()
        self.front = self.front.getNext()
        if self.isEmpty():
            self.back = None

        return front

    def print(self):
        tmp = self.front
        while tmp is not None:
            print(tmp.getValue(), end=" -> ")
            tmp = tmp.getNext()

        print()


if __name__ == "__main__":
    from random import randint, shuffle

    queue = PriorityQueue()
    lst = [x for x in range(10)]
    shuffle(lst)
    print(lst)

    for i in lst:
        queue.enqueue(i)
    queue.print()
