from nearestNeighbor import NearestNeighbor
from sys import argv
import time
from twoOpt import TwoOpt
from TspPath import Path
import xlrd
from Node import Node

def generateFile(data, method):
    if method == 1:
        results_file = open('results_k.csv', 'a+')
    elif method == 2:
        results_file = open('results_alpha.csv', 'a+')
    data_str = ''
    for d in range(len(data)):
        if d == len(data) - 1:
            data_str += str(data[d]) + '\n'
        else:
            data_str += str(data[d]) + '; '
    results_file.write(data_str)
    results_file.close()

"""
description: Read each line and get the data of each node
params: line, The current line of the file
return: list with the idx, and cordinates of each node
"""
def getCoordinates(line):
    data = line.split()

    if len(data) == 3:
        try:
            coordinates = (str(data[0]), float(data[1]), float(data[2]))
            return coordinates
        except ValueError:
            pass

    return None

"""
description: Get the set of nodes from the file pased
return: the set of all the nodes
"""
def getNodes(node_file):
    rfile = open(node_file, 'r')
    nodes = []

    for line in rfile:
        if 'optimal' in line:
            break
        coordinates = getCoordinates(line)
        nodes.append(Node(coordinates))
    rfile.close()

    return nodes

def main():
    start = time.time()
    k = 1
    alpha = 0
    min_distance = 999999999999

    # Get file by param
    if len(argv) < 2:
        print("Please enter the file name.")
        exit()
    node_file = argv[1]
    
    # Number of global iterations
    if len(argv) >= 3:
        globalIterations = int(argv[2])
    else:
        globalIterations = 1

    # Get 2opt execution time (minutes)
    if len(argv) >= 4:
        twoOptTime = float(argv[3]) * 60
    else:
        twoOptTime = 179.0

    c =  'Method\n'
    c += '1) K-Best\n'
    c += '2) RCL\n'
    c += 'method: '
    method = int(input(c))

    if method == 1:
        k = int(input('K: '))

    if method == 2:
        alpha = float(input('ALPHA (0 a 1): '))

    globalTime = float(input('Global time: ')) * 60

    nodes = getNodes(node_file)
    optimal = 0
    rfile = open(node_file, 'r')
    for line in rfile:
        if 'optimal' in line:
            data = line.split()
            optimal = int(data[len(data) - 1])
    rfile.close()

    currentIteration = 0
    while True:
        nearest_neighbor = NearestNeighbor(nodes, k, alpha, method)
        tour = nearest_neighbor.run()

        twoOpt = TwoOpt(tour, twoOptTime)
        neighbor_tour = twoOpt.run()
        # Path(neighbor_tour)

        distance = twoOpt.distanceTour(neighbor_tour)
        if distance < min_distance:
            min_distance = distance
            min_tour_path = twoOpt.resultPath(neighbor_tour)
            min_tour = neighbor_tour

        currentIteration += 1
        if currentIteration >= globalIterations:
            break

        if (time.time() - start) > globalTime:
            break

    print('----- Final Result -----\n')
    end = time.time()
    elapsed = round((end - start) * 100) / 100
    print(f'Minimum tour: {min_tour_path}')
    print(f'Minimum distance: {min_distance}')
    print(f'Time of execution: {elapsed}')

    data = []
    data.append(argv[1][7:])
    data.append(globalIterations if len(argv) >= 3 else 1)
    data.append(twoOptTime if len(argv) >= 4 else 180.0)
    if method == 1:
        data.append(k)
    elif method == 2:
        data.append(alpha)
    data.append(elapsed)
    data.append(min_distance)
    data.append(optimal)
    data.append(str(round((1 - optimal / min_distance) * 10000) / 100) + '%')

    generateFile(data, method)
    Path(min_tour)

if __name__ == '__main__':
    main()
