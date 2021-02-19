
class BucketQueue:

    def __init__(self) -> None:
        self.buckets = [[]]*100
        self.contains = set()

    def isEmpty(self):
        return len(self.contains) == 0

    def enqueue(self, priority, value):
        while priority >= len(self.buckets):
            self.buckets.append([])

        self.buckets[priority].append(value)
        self.contains.add(value)

    def removeMin(self):
        i = 0
        while self.buckets[i] == []:
            i += 1

        value = self.buckets[i].pop()
        self.contains.remove(value)
        return value

    def hasValue(self, value):
        return value in self.contains
