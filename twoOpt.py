import time
import math

class TwoOpt():
    def __init__(self, route, timeAvailable):
        self.route = route
        self.start = start = time.time()
        self.end = start + timeAvailable

    def run(self):
        improvement = True
        s = self.route
        while improvement:
            improvement = False
            best_distance = self.distanceTour(s)
            i = 1
            while i < len(s):
                for k in range(i+1, len(s)):
                    new_route = self.twoOptSwap(s, i, k)
                    new_distance = self.distanceTour(new_route)
                    if new_distance < best_distance:
                        s = new_route
                        best_distance = new_distance
                        improvement = True
                        i = 1
                    if time.time() > self.end:
                        return s
                else:
                    i += 1
        return s

    def twoOptSwap(self, route, i, k):
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

    def distanceTour(self, route):
        tot = 0
        for idx in range(0, len(route)-1):
            tot += route[idx].distance(route[idx+1])
        tot += route[len(route)-1].distance(route[0])

        return tot

    def resultPath(self, path=None):
        result_path = ''

        if path == None:
            path = self.route

        for i in range(0, len(path)):
            if i == len(path) - 1:
                result_path += path[i].idx
            else:
                result_path += path[i].idx + ' -> '

        return result_path
