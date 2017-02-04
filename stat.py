"""
Collect the statistics of the KMeans performance
"""

from kmeans import *

numberofexp = 10000
clusterscnt = [0, 0, 0]

for expidx in range(numberofexp):
    if expidx % 200 == 0:
        print '{} / {}'.format(expidx, numberofexp)
    filename = 'hw1.2-data.txt'
    points = readfromtext(filename)
    clusters = rdinitcluster()
    while True:
        changed = assigncluster(points, clusters)
        if not changed:
            break
        updatecluster(points, clusters)
    effectiveclustercnt = 0
    for cluster in clusters:
        if len(cluster[1]) > 0:
            effectiveclustercnt += 1
    clusterscnt[effectiveclustercnt - 1] += 1

for i in range(3):
    print clusterscnt[i], float(clusterscnt[i]) / numberofexp
