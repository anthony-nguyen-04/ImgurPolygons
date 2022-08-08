
import numpy as np

# we need to reverse it because numpy does (0,0)
# as top-left corner instead of bottom-left
def checkDirection(zCross):
    if zCross > 0:
        # return 0
        return 1
        # "CLOCKWISE"
    elif zCross < 0:
        # return 1
        return 0
        # "COUNTER-CLOCKWISE"
    else:
        print("COLLINEAR")
        return -1
        # "N/A"

def checkPolygon(points):

    # sorts points by y-value
    ascendingPoints = sorted(points.items(), key=lambda z: z[1][1])

    # from lowest y-value vertices, find the one with highest x-value
    # ensures that at least one of its adjacent vertices does not have same y-value
    bottomLevelPoints = [z for z in ascendingPoints if z[1][1] == (ascendingPoints[0])[1][1]]
    bottomLevelPoints = sorted(bottomLevelPoints, key=lambda z: z[1][0])
    bottomPoint = bottomLevelPoints[-1]
    bottomIndex = bottomPoint[0]

    # uses a separate algorithm (based off of cross product of vectors from bottom-most point)
    # solves for orientation of polygon

    # used to get vectors originating from "bottom" vertex
    x, y = points[bottomIndex]

    xBefore, yBefore = points[(bottomIndex - 1) % len(points)]
    xAfter, yAfter = points[(bottomIndex + 1) % len(points)]

    # calculates vectors from vertex
    vectorBefore = (xBefore - x, yBefore - y)
    vectorAfter = (xAfter - x, yAfter - y)

    vectorBefore = np.asarray(vectorBefore)
    vectorAfter = np.asarray(vectorAfter)

    # cross product of vectors originating from bottom-most vertex
    cross = np.cross(vectorBefore, vectorAfter)

    # from the cross product, solves for orientation
    calculatedOrientation = checkDirection(cross)

    if calculatedOrientation == 0:
        #print("%s : CW" % i)
        return("CW")
    elif calculatedOrientation == 1:
        #print("%s : CCW" % i)
        return("CCW")
    else:
        raise Exception('collinear points -- exiting')