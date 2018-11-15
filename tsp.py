import math
import sys
import time
from TspPath import Path

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.visited = False

def calculateDistance(city1, city2):
    x_distance = abs(city1.x - city2.x)
    y_distance = abs(city1.y - city2.y)

    return int(round(math.sqrt(x_distance * x_distance + y_distance * y_distance)))

def fileImport(filename):
    with open(filename, "r") as myfile:
        Nodes = []
        for line in myfile:
            numArray = []
            lineNumbers = line.split()
            for num in lineNumbers:
                numArray.append(int(num))
            Nodes.append(Node(numArray[0], numArray[1], numArray[2]))

    return Nodes

def fileExport(filename, tour, distance):
    with open(filename + ".tour", "w") as myFile:
        myFile.write(str(distance) + '\n')
        for city in tour:
            myFile.write("%d\n" % city.id)

def calculateTotalDistance(route):
    tot = 0
    for idx in range(0, len(route)-1):
        tot += calculateDistance(route[idx], route[idx+1])
    tot += calculateDistance(route[len(route)-1], route[0])

    return tot

def findClosestNeighbor(v, route):
    shortestEdgeLength = 99999999999
    closestNeighbor = None
    for c in route:
        if c.id != v.id:
            distance = calculateDistance(v, c)
            if shortestEdgeLength > distance:
                closestNeighbor = c
                shortestEdgeLength = distance

    return closestNeighbor

def nearestNeighbor(route):
    new_route = []
    current_node = route.pop(0)
    new_route.append(current_node)
    while route != []:
        next = findClosestNeighbor(current_node, route)
        current_node = next
        route.remove(next)
        new_route.append(current_node)

    return new_route

def twoOptSwap(route, i, k):
    new_route = []

    # 1. take route[0] to route[i-1] and add them in order to new_route
    for index in range(0, i):
        new_route.append(route[index])

    # 2. take route[i] to route[k] and add them in reverse order to new_route
    for index in range(k, i-1, -1):
        new_route.append(route[index])

    # 3. take route[k+1] to end and add them in order to new_route
    for index in range(k+1, len(route)):
        new_route.append(route[index])

    return new_route

def findTSPSolution(s, timeAvailable):
    improvement = True
    start = time.time()
    end = start + timeAvailable
    while improvement:
        improvement = False
        best_distance = calculateTotalDistance(s)
        i = 1
        while i < len(s):
            for k in range(i+1, len(s)):
                new_route = twoOptSwap(s, i, k)
                new_distance = calculateTotalDistance(new_route)
                if new_distance < best_distance:
                    s = new_route
                    best_distance = new_distance
                    improvement = True
                    i = 1
                if time.time() > end:
                    return s
            else:
                i += 1

    return s

def printTour(s):
    sys.stdout.write("ORDER: ")
    for c in s:
        sys.stdout.write(str(c.id) + ' ')
    print('/n')
    print("Distance: " + str(calculateTotalDistance(s)))

def main():
    start = time.time()

    if len(sys.argv) < 2:
        print("Please enter the file name.")
        exit()
    filename = sys.argv[1]

    if len(sys.argv) == 3:
        totalTime = float(sys.argv[2]) * 60 - 1
    else:
        totalTime = 179.0

    s = fileImport(filename)

    greedy = nearestNeighbor(s)
    s = fileImport(filename)

    print("\nAFTER NEAREST NEIGHBOR PASS")
    printTour(greedy)

    if calculateTotalDistance(greedy) < calculateTotalDistance(s):
        s = greedy
    else:
        print("Greedy solution discarded.")

    timeAvailable = totalTime - (time.time() - start)
    s = findTSPSolution(s, timeAvailable)
    s.append(s[0])
    fileExport(filename, s, calculateTotalDistance(s))

    print("\nAFTER 2OPT")
    printTour(s)
    end = time.time()
    timeElapsed = end - start
    print("TIME ALLOCATED: %f" % (totalTime + 1))
    print("TIME USED: %f" % timeElapsed)
    Path(s)

if __name__ == "__main__":
    main()