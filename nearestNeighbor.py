import random
from operator import itemgetter

class NearestNeighbor():
    def __init__(self, nodes, k=1, alpha=0, method=1):
        self.nodes = nodes
        self.tour = []
        self.k = k
        self.alpha = alpha
        self.method = method

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
