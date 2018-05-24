import sys
from city import City
from neighbour import Neighbour
from board import Board
from results import Results

def printResults(search, results):
    print("\n" + search + " =============")
    print("avgSpace: " + str(results.avgSpace))
    print("avgTime: " + str(results.avgTime))
    print("runningTime: " + str(results.runningTime))
    print("avgPathLen: " + str(results.avgPathLen))
    print("problemsSolved: " + str(results.problemsSolved))

bfsResults = Results()
dfsResults = Results()
idsResults = Results()
gbfsResults = Results()
astarResults = Results()

for i in range(100):
    board = Board(100, 26, 4)
    bfsResults += board.BFS()
    dfsResults += board.DFS()
    idsResults += board.IDS()
    gbfsResults += board.GBFS()
    astarResults += board.ASTAR()

printResults("BFS", bfsResults)
printResults("DFS", dfsResults)
printResults("IDS", idsResults)
printResults("GBFS", gbfsResults)
printResults("ASTAR", astarResults)

# print the board if argument 2 is draw
if len(sys.argv) >= 2:
    if sys.argv[1] == '--drawBFS':
        board.draw(bfsResults.path)
    if sys.argv[1] == '--drawDFS':
        board.draw(dfsResults.path)
    if sys.argv[1] == '--drawIDS':
        board.draw(idsResults.path)
    if sys.argv[1] == '--drawGBFS':
        board.draw(gbfsResults.path)
    if sys.argv[1] == '--drawASTAR':
        board.draw(astarResults.path)