import numpy as np
import matplotlib.pyplot as plt

class Path:
    def __init__(self, nodes):
        xs = []
        ys = []

        for node in nodes:
            xs.append(node.x)
            ys.append(node.y)

        plt.plot(xs, ys, '-ro')
        plt.show()
