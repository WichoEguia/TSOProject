from nearestNeighbor import NearestNeighbor
from sys import argv
import time
from twoOpt import TwoOpt
from TspPath import Path
import xlrd

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

def main():
    start = time.time()
    k = 1
    alpha = 0
    min_distance = 999999999999

    # Get file by param
    if len(argv) < 2:
        print("Please enter the file name.")
        exit()
    filename = argv[1]
    
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
        nearest_neighbor = NearestNeighbor(filename, k, alpha, method)
        tour = nearest_neighbor.run()

        twoOpt = TwoOpt(tour, twoOptTime)
        neighbor_tour = twoOpt.run()

        distance = twoOpt.distanceTour(neighbor_tour)
        if distance < min_distance:
            min_distance = distance
            min_tour_path = twoOpt.resultPath(neighbor_tour)
            min_tour = neighbor_tour

        # if (time.time() - start) > (60 * 2):
        #     break

    print('----- Final Result -----\n')
    end = time.time()
    elapsed = round((end - start) * 100) / 100
    print(f'Minimum tour: {min_tour_path}')
    print(f'Minimum distance: {min_distance}')
    print(f'Time of execution: {elapsed}')

    data = []
    data.append(argv[1][7:])
    data.append(globalIterations if len(argv) >= 3 else 1)
    data.append(twoOptTime + 1 if len(argv) >= 4 else 180.0)
    if method == 1:
        data.append(k)
    elif method == 2:
        data.append(alpha)
    data.append(elapsed)
    data.append(min_distance)

    generateFile(data, method)
    Path(min_tour)

if __name__ == '__main__':
    main()
