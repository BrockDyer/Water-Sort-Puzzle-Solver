
class BucketQueue:

    def __init__(self, size=100) -> None:
        self.buckets = [[] for x in range(size)]
        self.contained = {}

    def isEmpty(self):
        return len(self.contained) == 0

    def enqueue(self, priority, value):
        while priority >= len(self.buckets):
            self.buckets.append([])

        self.buckets[priority].append(value)
        if value not in self.contained:
            self.contained[value] = 0
        self.contained[value] += 1

    def removeMin(self):
        i = 0
        while self.buckets[i] == []:
            i += 1

        value = self.buckets[i].pop()
        self.contained[value] -= 1
        if self.contained[value] == 0:
            del self.contained[value]
        return value

    def hasValue(self, value):
        return value in self.contained

    def __str__(self):
        result = ""
        for bucket in self.buckets:
            for value in bucket:
                result += str(value) + " -> "

        return result


if __name__ == "__main__":
    from random import shuffle

    queue = BucketQueue(10)

    nums = [x for x in range(10)]
    shuffle(nums)

    print(nums)

    for x in nums:
        queue.enqueue(x, x)
        # print(queue)

    result = ""
    while not queue.isEmpty():
        result += str(queue.removeMin()) + " -> "

    print(result)
