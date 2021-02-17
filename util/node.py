class Node:

    def __init__(self, value) -> None:
        self.value = value
        self.next = None

    def getValue(self):
        return self.value

    def getNext(self):
        return self.next

    def setNext(self, next: "Node"):
        self.next = next

    def setValue(self, value):
        self.value = value
