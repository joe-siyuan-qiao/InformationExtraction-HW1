"""
Read the points from test file and do k-means on them
"""

import random as rd, math, matplotlib.pyplot as plt
from copy import deepcopy


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def readfromtext(filename):
    points = []
    fin = open(filename, 'r')
    while True:
        line = fin.readline()
        if line == '':
            break
        line = line.split()
        points.append([float(line[0]), float(line[1]), -1])
    fin.close()
    return points


def rdinitcluster():
    clusters = []
    for i in range(3):
        center = [rd.random(), rd.random()]
        clusters.append([deepcopy(center), []])
    return clusters


def assigncluster(points, clusters):
    changed = 0
    for cluster in clusters:
        del cluster[1][:]
    for pidx in range(len(points)):
        cidx_ori, cidx_new, mindist = points[pidx][2], -1, 1e5
        for cidx in range(len(clusters)):
            dist = distance(points[pidx], clusters[cidx][0])
            if dist < mindist:
                cidx_new, mindist = cidx, dist
        if cidx_new != cidx_ori:
            changed = 1
        points[pidx][2] = cidx_new
        clusters[cidx_new][1].append(pidx)
    return changed


def updatecluster(points, clusters):
    for cluster in clusters:
        x_acc, y_acc, n_acc = 0.0, 0.0, 0
        for pidx in cluster[1]:
            x_acc, y_acc = x_acc + points[pidx][0], y_acc + points[pidx][1]
            n_acc = n_acc + 1
        if n_acc > 0:
            x_acc, y_acc = x_acc / n_acc, y_acc / n_acc
            cluster[0] = [x_acc, y_acc]


def visualize(points, clusters, img_name):
    plot_settings = ['or', 'vb', '*g', 'oc', 'vc', '*c']
    if clusters[0][0][0] < clusters[1][0][0]:
        plot_settings[0], plot_settings[1] = plot_settings[1], plot_settings[0]
        plot_settings[3], plot_settings[4] = plot_settings[4], plot_settings[3]
    if clusters[0][0][0] < clusters[2][0][0]:
        plot_settings[0], plot_settings[2] = plot_settings[2], plot_settings[0]
        plot_settings[3], plot_settings[5] = plot_settings[5], plot_settings[3]
    if clusters[1][0][0] < clusters[2][0][0]:
        plot_settings[1], plot_settings[2] = plot_settings[2], plot_settings[1]
        plot_settings[4], plot_settings[5] = plot_settings[5], plot_settings[4]
    for cidx in range(3):
        xlist, ylist = [], []
        for pidx in clusters[cidx][1]:
            xlist.append(points[pidx][0])
            ylist.append(points[pidx][1])
        plt.plot(xlist, ylist, plot_settings[cidx])
    for cidx in range(3):
        cluster = clusters[cidx]
        plt.plot([cluster[0][0]], [cluster[0][1]], plot_settings[cidx+3],
                 markersize=15)
    plt.savefig(img_name)
    plt.clf()


if __name__ == '__main__':
    filename = 'hw1.2-data.txt'
    print '| reading file {}'.format(filename)
    points = readfromtext(filename)
    print '| initialize clusters at random'
    clusters = rdinitcluster()
    img_cnt = 0
    while True:
        changed = assigncluster(points, clusters)
        if not changed:
            break
        updatecluster(points, clusters)
        visualize(points, clusters, '{}.pdf'.format(img_cnt))
        img_cnt += 1
