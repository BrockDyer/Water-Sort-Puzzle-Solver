from .node import Node


class Stack:

    def __init__(self) -> None:
        self._top = None
        self.size = 0

    def isEmpty(self):
        return self._top is None

    def getSize(self):
        return self.size

    def push(self, value):
        node = Node(value)
        node.setNext(self._top)
        self._top = node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise IndexError("Tried to pop from empty stack")

        top = self._top.getValue()
        self._top = self._top.next
        self.size -= 1
        return top

    def top(self):
        if self.isEmpty():
            raise IndexError("Tried to get top of empty stack")

        top = self._top.getValue()
        return top

    def reverse(self):
        tmp = Stack()
        while not self.isEmpty():
            tmp.push(self.pop())
        self._top = tmp._top
        self.size = tmp.size
        return self

    def getTopNode(self):
        if self.isEmpty():
            raise IndexError("Tried to get top of empty stack")
        return self._top
