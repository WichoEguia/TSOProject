from math import hypot

class Node:
    def __init__(self, cors):
        self.idx = cors[0]
        self.x = cors[1]
        self.y = cors[2]

    def __str__(self):
        return str(self.idx)

    def __eq__(self, otherNode):
        return self.__dict__ == otherNode.__dict__

    def distance(self, otherNode):
        dx = self.x - otherNode.x
        dy = self.y - otherNode.y
        return int(hypot(dx, dy))