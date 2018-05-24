import random

class Point:
    def __init__(self, dimension):
        self.x = int(round(random.random() * dimension))
        self.y = int(round(random.random() * dimension))

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y