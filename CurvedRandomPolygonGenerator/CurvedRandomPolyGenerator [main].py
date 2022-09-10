import random
from main_improved import makePolygon
from ChaikinPolygon import smoothPolygon
from ImgurPolygons.PolygonChecker import checkPolygon

import matplotlib.pyplot as plt
import matplotlib.lines as lines

# default CW
def generatePoints(numVertices):
    #points = {}
    points = []
    for i in range(numVertices):
        x = random.random()
        y = random.random()

        #points[i] = ([x,y])
        points.append(([x, y]))

    return points

# def reversePoints(points):
#     pointsNew = {}
#     pointsNew[0] = points[0]
#     print(pointsNew[0])
#     for i in range(1, len(points)):
#         pointsNew[i] = points[len(points) - i]
#
#     print("points")
#     print(points)
#     print(pointsNew)
#
#     return pointsNew

def main():
    orientation = random.randint(0,1)
    print(orientation)

    pointz = generatePoints(100)
    print(pointz)

    polygon = makePolygon(pointz)
    print(polygon)

    orderedPoints = {}

    for i in range(len(polygon)):
        if i == 0:
            orderedPoints[0] = polygon[0]
        else:
            if orientation == 0:
                orderedPoints[i] = polygon[i]
            else:
                orderedPoints[i] = polygon[len(polygon) - i]

    # pointz = generatePoints(10)
    # pointzValues = pointz.values()
    # polygon = makePolygon(pointzValues)
    #
    # print(polygon)
    #
    # if orientation == 1:
    #     start = polygon[0]
    #     polygon = list(reversed(polygon[1:]))
    #     polygon.insert(0, start)
    #     pointz = reversePoints(pointz)
    #     polygon = makePolygon(pointz.values())
    #
    #     print(polygon)

    smoothed_polygon = smoothPolygon(polygon)
    calculatedOrientation = checkPolygon(orderedPoints, numpy=False)
    print(calculatedOrientation)

    f1 = plt.figure(1)
    plt.xlim(-0.25, 1.25)
    plt.ylim(-0.25, 1.25)


#    pset = polygon
    pset = list(orderedPoints.values())
    pset.append(pset[0])
    xs, ys = zip(*pset)
    f1.gca().plot(xs, ys)

    f1.gca().text(xs[0], ys[0], "0")
    f1.gca().text(xs[1], ys[1], "1")
    f1.gca().text(xs[2], ys[2], "2")
    f1.gca().text(xs[3], ys[3], "3")
    f1.gca().text(xs[4], ys[4], "4")
    # f1.gca().text(xs[int(len(xs) / 4)], ys[int(len(xs) / 4)], "1")
    # f1.gca().text(xs[int(len(xs) / 2)], ys[int(len(xs) / 2)], "2")
    # f1.gca().text(xs[int(len(xs) / 1.33)], ys[int(len(xs) / 1.33)], "3")

    f1.gca().text(0.5, 0.85, calculatedOrientation)
    #print(calculatedOrientation)

    f2 = plt.figure(2)
    plt.xlim(-0.25, 1.25)
    plt.ylim(-0.25, 1.25)

    smoothX = [i for i, j in smoothed_polygon]
    smoothX.append(smoothX[0])

    smoothY = [j for i, j in smoothed_polygon]
    smoothY.append(smoothY[0])

    myline = lines.Line2D(smoothX, smoothY, color='r')
    f2.gca().add_artist(myline)

    plt.show()


if __name__ == "__main__":
    main()
