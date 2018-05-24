import string, pygame, math, time
from heapq import heappush, heappop
from point import Point
from city import City
from results import Results
from random import randrange
from collections import deque

class Board:
    def __init__(self, dimension, cityCount, maxNeighbourCount):
        self.cities = []
        self.dimension = dimension
        self.buildCities(cityCount, maxNeighbourCount)

        # Randomly select start and goal cities
        startIndex = randrange(0, len(self.cities))
        goalIndex = randrange(0, len(self.cities))

        while (startIndex == goalIndex):
            goalIndex = randrange(0, len(self.cities))

        self.start = self.cities[startIndex]
        self.goal = self.cities[goalIndex]

        # Calculate euclidean and manhattan distance to goal from each city
        for city in self.cities:
            city.euclideanDistance = math.sqrt((city.point.x - self.goal.point.x)**2 + (city.point.y - self.goal.point.y)**2)

    def __str__(self):
        boardStr = ""
        for city in self.cities:
            boardStr += str(city) + "\n"
        return boardStr

    'Build cities for the board with distinct coordinates'
    def buildCities(self, cityCount, maxNeighbourCount):
        # Build the cities
        for cityNumber in range(0, cityCount):
            point = Point(self.dimension)
        
            # Ensure that the point is distinct from existing cities
            while self.pointOccupied(point):
                point = Point(self.dimension)

            name = string.ascii_uppercase[cityNumber]
            city = City(point, name)
            self.cities.append(city)
        
        # Connect cities
        for city in self.cities:
            city.addNeighbours(self.cities, maxNeighbourCount)

    'Determine if a given point already contains a city'
    def pointOccupied(self, point):
        for city in self.cities:
            if point == city.point:
                return True
        return False
    
    'Draw the board and optionally a provided path'
    def draw(self, path=[]):
        # Initalize window and draw board
        pygame.display.init()
        pygame.font.init()
        screen = pygame.display.set_mode((530, 530))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 510, 510))

        # Draw every city on the board
        for city in self.cities:
            text = city.name
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            color = (175, 175, 175)
            if city == self.start:
                color = (0, 0, 255)
            elif city == self.goal:
                color = (255, 0, 0)
            text = font.render(text, True, color)
            screen.blit(text, (city.point.x * 5, city.point.y * 5))

            for neighbour in city.neighbours:
                pygame.draw.line(screen, (210, 210, 210), city.getPointForDrawing(), neighbour.city.getPointForDrawing())

            # Draw the path from start to goal
            if path:
                for city, nextCity in zip(path, path[1:]):
                    pygame.draw.line(screen, (0, 255, 0), city.getPointForDrawing(), nextCity.getPointForDrawing(), 3)

        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == 12:
                    running = False    

    def getPathFromParents(self):
        path = [self.goal]
        city = self.goal
        while not city == self.start:
            city = self.parents[city]
            path.insert(0, city)
        return path
    
    def getPathDistance(self, path):
        distance = 0
        for index, city in enumerate(path[:-1]):
            nextCity = path[index+1]
            for neighbour in city.neighbours:
                if neighbour.city == nextCity:
                    distance += neighbour.distance
        
        return distance
    
    def BFS(self):        
        # Time how long it takes to get a path
        results = Results()
        start = time.clock()
        results.path = self.__BFS(results)
        end = time.clock()

        # Determine results
        results.runningTime = end - start
        if results.path:
            results.problemsSolved = 1
            results.avgPathLen = self.getPathDistance(results.path)
        
        return results
    
    def __BFS(self, results):
        # Reset values before searching
        queue = deque([self.start])
        self.parents = dict()
        self.visited = set()

        # Traverse the graph looking for the goal city
        while queue:
            # Get the next city to visit
            city = queue.popleft()
            self.visited.add(city)
            results.avgTime += 1

            # A path has been found to the goal, stop searching
            if city == self.goal:
                return self.getPathFromParents()

            # Check every adjacent city
            for neighbour in city.neighbours:
                # Check if this city has already been visited
                if neighbour.city in self.visited:
                    continue
                self.parents[neighbour.city] = city
                queue.append(neighbour.city)
                results.avgSpace = max(results.avgSpace, len(queue))

        # No solution found
        return None
    
    def DFS(self):
        # Time how long it takes to get a path
        results = Results()
        start = time.clock()
        results.path = self.__DFS(results)
        end = time.clock()

        # Determine results
        results.runningTime = end - start
        if results.path:
            results.problemsSolved = 1
            results.avgPathLen = self.getPathDistance(results.path)

        return results

    def __DFS(self, results, maxDepth=math.inf):
        # Reset values before searching
        cityDepth = dict()
        cityDepth[self.start] = 0
        stack = [self.start]
        self.parents = dict()
        self.visited = set()

        # Traverse the graph looking for the goal city
        while stack:
            # Get the next city to visit
            city = stack.pop()
            self.visited.add(city)
            results.avgTime += 1

            # A path has been found to the goal, stop searching
            if city == self.goal:
                return self.getPathFromParents()

            # Max depth has been reached without finding the goal
            if cityDepth[city] > maxDepth:
                continue

            # Check every adjacent city
            for neighbour in city.neighbours:
                # Check if this city has already been visited
                if neighbour.city in self.visited:
                    continue

                # Record the parent and depth for the neighbour city
                self.parents[neighbour.city] = city
                cityDepth[neighbour.city] = cityDepth[city] + 1
                # Add city to stack
                stack.append(neighbour.city)
                results.avgSpace = max(results.avgSpace, len(stack))

        # No solution found
        return None

    def IDS(self):
        # Time how long it takes to get a path
        results = Results()
        start = time.clock() 

        depth = 1
        while depth <= len(self.cities) and not results.path:
            results.path = self.__DFS(results, depth)
            depth += 1
        end = time.clock()

        # Determine results
        results.runningTime = end - start
        if results.path:
            results.problemsSolved = 1
            results.avgPathLen = self.getPathDistance(results.path)

        return results

    def GBFS(self):        
        # Time how long it takes to get a path
        results = Results()
        start = time.clock()
        results.path = self.__GBFS(results)
        end = time.clock()

        # Determine results
        results.runningTime = end - start
        if results.path:
            results.problemsSolved = 1
            results.avgPathLen = self.getPathDistance(results.path)
        
        return results

    def __GBFS(self, results):
        # Reset values before searching
        heap = []
        heappush(heap, (self.start.euclideanDistance, self.start))
        self.parents = dict()
        self.visited = set()

        # Traverse the graph looking for the goal city
        while heap:
            # Get the next city to visit
            city = heappop(heap)
            city = city[1]
            self.visited.add(city)
            results.avgTime += 1

            # A path has been found to the goal, stop searching
            if city == self.goal:
                return self.getPathFromParents()

            # Check every adjacent city
            for neighbour in city.neighbours:
                # Check if this city has already been visited
                if neighbour.city in self.visited:
                    continue
                self.parents[neighbour.city] = city
                heappush(heap, (neighbour.city.euclideanDistance, neighbour.city))
                results.avgSpace = max(results.avgSpace, len(heap))

        # No solution found
        return None

    def ASTAR(self):        
        # Time how long it takes to get a path
        results = Results()
        start = time.clock()
        results.path = self.__ASTAR(results)
        end = time.clock()

        # Determine results
        results.runningTime = end - start
        if results.path:
            results.problemsSolved = 1
            results.avgPathLen = self.getPathDistance(results.path)
        return results

    def __ASTAR(self, results):
        # Reset values before searching
        heap = []
        heappush(heap, (0, self.start))
        self.parents = dict()
        self.visited = set()

        # Traverse the graph looking for the goal city
        while heap:
            # Get the next city to visit
            city = heappop(heap)
            city = city[1]
            self.visited.add(city)
            results.avgTime += 1

            # A path has been found to the goal, stop searching
            if city == self.goal:
                return self.getPathFromParents()

            # Check every adjacent city
            for neighbour in city.neighbours:
                # Check if this city has already been visited
                if neighbour.city in self.visited:
                    continue
                self.parents[neighbour.city] = city

                # cost so far to reach n
                neighbour.city.distanceSoFar = city.distanceSoFar + neighbour.distance
                estimatedDistance = neighbour.city.distanceSoFar + neighbour.city.euclideanDistance
                heappush(heap, (estimatedDistance, neighbour.city))
                results.avgSpace = max(results.avgSpace, len(heap))

        # No solution found
        return None

    
