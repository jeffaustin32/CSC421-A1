class Results:
    def __init__(self):
        self.avgSpace = 0
        self.avgTime = 0
        self.runningTime = 0
        self.avgPathLen = 0
        self.problemsSolved = 0
        self.path = []
    
    def __add__(self, other):
        newResults = Results()
        newResults.avgSpace = (self.avgSpace + other.avgSpace)
        newResults.avgTime = (self.avgTime + other.avgTime)
        newResults.avgPathLen = (self.avgPathLen + other.avgPathLen)
        newResults.runningTime = self.runningTime + other.runningTime
        newResults.problemsSolved = self.problemsSolved + other.problemsSolved
        newResults.path = other.path

        if self.avgSpace and other.avgSpace:
            newResults.avgSpace = newResults.avgSpace / 2
        if self.avgTime and other.avgTime:
            newResults.avgTime = newResults.avgTime / 2
        if self.avgPathLen and other.avgPathLen:
            newResults.avgPathLen = newResults.avgPathLen / 2

        return newResults