"""
Command: py TSP-grasp_nearest_neighbor.py file_path number_of_iterations
"""

from Node import Node
from sys import argv
import random
import time
from operator import itemgetter
from twoOpt import TwoOpt
from TspPath import Path

class NearestNeighbor():
    def __init__(self, k=1, alpha=0, method=1):
        self.nodes = self.getNodes()
        self.tour = []
        self.k = k
        self.alpha = alpha
        self.method = method

    """
    description: Get the set of nodes from the file pased
    return: the set of all the nodes
    """
    def getNodes(self):
        rfile = open(argv[1], 'r')
        nodes = []

        for line in rfile:
            coordinates = self.getCoordinates(line)
            nodes.append(Node(coordinates))

        return nodes

    """
    description: Read each line and get the data of each node
    params: line, The current line of the file
    return: list with the idx, and cordinates of each node
    """
    def getCoordinates(self, line):
        data = line.split()
        
        if len(data) == 3:
            try:
                coordinates = (str(data[0]), float(data[1]), float(data[2]))
                return coordinates
            except ValueError:
                pass

        return None

    """
    description: Run the algorithm and get the tour
    return: tour of nodes
    """
    def run(self):
        current = self.nodes[0]

        while len(self.nodes) != len(self.tour):
            self.tour.append(current)
            arr_nodes = []

            for node in self.nodes:
                if node not in self.tour:
                    distance = current.distance(node)

                    arr_nodes.append({
                        'distance': distance,
                        'node': node
                    })

            if len(arr_nodes) > 0:
                if self.method == 1:
                    current = self.getKbestNode(arr_nodes)
                elif self.method == 2:
                    current = self.getRCLNode(arr_nodes)

            else:
                break

        self.tour.append(self.tour[0])
        return self.tour

    """
    description: select randomly a node
    return: selected node
    """
    def getKbestNode(self, arr_opts):
        arr_opts = sorted(arr_opts, key=itemgetter('distance'))
        arr_kbest = []
        counter = 0

        for i in range(0, len(arr_opts)):
            if counter < self.k:
                arr_kbest.append(arr_opts[i])
                counter += 1
        

        index_rdm = random.randint(0, len(arr_kbest) - 1)
        selected = arr_kbest[index_rdm]

        return selected['node']

    """
    description: Get the register candidate list
    return: selected node 
    """
    def getRCLNode(self, arr_opts):
        arr_opts = sorted(arr_opts, key=itemgetter('distance'))
        cmin = arr_opts[0]['distance']
        cmax = arr_opts[len(arr_opts)-1]['distance']
        rcl = []

        for opt in arr_opts:
            if cmin <= opt['distance'] <= cmin + self.alpha * (cmax - cmin):
                rcl.append(opt)

        index_rdm = random.randint(0, len(rcl) - 1)
        selected = rcl[index_rdm]
        return selected['node']

    """
    description: Calculate the distance in a array of nodes
    return: integer, distance
    """
    def distanceTour(self, path=None):
        distance = 0

        if path == None:
            path = self.tour

        for i in range(len(path)):
            distance += int(path[i].distance(path[i + 1]))
            if i + 1 == len(path) - 1:
                break

        return distance

    """
    description: Maxe a string with all nodes on the route
    return: String tour
    """
    def resultPath(self, path=None):
        result_path = ''

        if path == None:
            path = self.tour

        for i in range(0, len(path)):
            if i == len(path) - 1:
                result_path += path[i].idx
            else:
                result_path += path[i].idx + ' -> '

        return result_path

def main():
    start = time.time()
    k = 1
    alpha = 0
    min_distance = 999999999999
    
    # Number of global iterations
    if len(argv) >= 3:
        globalIterations = int(argv[2])
    else:
        globalIterations = 1

    # Get 2opt execution time (minutes)
    if len(argv) >= 4:
        twoOptTime = float(argv[3]) * 60 - 1
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

    for i in range(0, globalIterations):
        nearest_neighbor = NearestNeighbor(k, alpha, method)
        tour = nearest_neighbor.run()

        twoOpt = TwoOpt(tour, twoOptTime)
        neighbor_tour = twoOpt.run()

        distance = twoOpt.distanceTour(neighbor_tour)
        if distance < min_distance:
            min_distance = distance
            min_tour_path = twoOpt.resultPath(neighbor_tour)
            min_tour = neighbor_tour

        if (time.time() - start) > (60 * 2):
            break

    print('----- Final Result -----\n')
    end = time.time()
    elapsed = end - start
    print(f'Minimum tour: {min_tour_path}')
    print(f'Minimum distance: {min_distance}')
    print(f'Time of execution: {elapsed}')
    Path(min_tour)

if __name__ == '__main__':
    main()
