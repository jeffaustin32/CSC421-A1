class Neighbour:
    def __init__(self, city, distance):
        self.city = city
        self.distance = distance

    def __lt__(self, neighbour):
        return self.distance < neighbour.distance
    
    def __repr__(self):
        return str((self.city.name, self.distance))

    def __hash__(self):
        return hash(self.city.name)

    def __eq__(self, otherNeighbour):
        return self.city.name == otherNeighbour.city.name and self.distance == otherNeighbour.distance