import math, random
from point import Point
from neighbour import Neighbour
from heapq import nsmallest

class City:
    def __init__(self, point, name):
        self.point = point
        self.name = name
        self.neighbours = set()
        self.euclideanDistance = 0
        self.distanceSoFar = 0
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name + " (" + str(self.point.x) + ", " + str(self.point.y) + ")"

    def __eq__(self, otherCity):
        return self.name == otherCity.name

    def __lt__(self, otherCity):
        return self.euclideanDistance < otherCity.euclideanDistance

    def __hash__(self):
        return hash(self.name)

    'Get an offset point to draw on board'
    def getPointForDrawing(self):        
        return (self.point.x * 5 + 10, self.point.y * 5 + 10)

    'Create links between a city and its neighbouring cities'
    def addNeighbours(self, cities, neighbourCount):
        newNeighbours = []

        # Add every city except self as a potential neighbour
        for city in cities:
            if city == self:
                continue
            
            distance = math.sqrt((self.point.x - city.point.x)**2 + (self.point.y - city.point.y)**2)
            newNeighbours.append(Neighbour(city, distance))
        
        # Choose randomly between and 1 and 4 of the closest five cities to keep
        newNeighbours = nsmallest(4, newNeighbours)
        random.shuffle(newNeighbours)
        numberToKeep = int(round(random.random() * 3)) + 1
        newNeighbours = set(newNeighbours[0:numberToKeep])
        self.neighbours = self.neighbours.union(newNeighbours)

        # Make the link to the new neighbours bi-directional
        for neighbour in newNeighbours:
            neighbour.city.neighbours.add(Neighbour(self, neighbour.distance))
