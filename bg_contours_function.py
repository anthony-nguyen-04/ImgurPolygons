import matplotlib.pyplot as plt
from skimage.segmentation import (morphological_chan_vese,
                                  checkerboard_level_set)
from bg_map import *
from skimage.io import imread
from skimage.color import gray2rgb
from pandas import DataFrame
from PolygonChecker import checkPolygon
import random
import numpy as np
import cv2

def bg_contours_func(imgur_url, orientation = random.randint(0,1)):
    # 0 is CW, 1 is CCW
    initial_orientation = orientation #random.randint(0,1)

    # Morphological ACWE
    #input_file = ".\images\star.png"

    img = imread(imgur_url)

    img = img.astype(np.uint8)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    img = cv2.resize(img, (600, 600))

    map = get_bg_map(img)

    map = np.where(map > 0.5, 1, 0).astype(np.float32)

    if np.count_nonzero(map) < 50:
        raise Exception("no foreground")

    # Initial level set
    init_ls = checkerboard_level_set(map.shape, 6)

    # List with intermediate results for plotting the evolution
    ls = morphological_chan_vese(map, num_iter=10, init_level_set=init_ls,
                                 smoothing=3)


    fig, ax = plt.subplots()
    ax.imshow(img, cmap="gray")
    ax.set_axis_off()
    tester = ax.contour(ls, [0.5], colors='r')
    #   ax.set_title("Morphological ACWE segmentation", fontsize=12)

    contour_list = [variable for variable in ((tester.collections)[0]).get_paths()]

    biggest_contour = sorted(contour_list, key= lambda z : len(z.vertices), reverse=True)[0]
    biggest_contour_vertices = biggest_contour.vertices
    int_contour = biggest_contour_vertices.astype(int)

    ordered_contour = enumerate(DataFrame(int_contour).drop_duplicates().values)
    ordered_contour = list(ordered_contour)

    ordered_contour_map = {}
    num_coords = len(ordered_contour)

    for i, coord in ordered_contour:

        # have to flip because numpy's coordinate convention

        # CCW
        if (initial_orientation == 1):
            ordered_contour_map[i] = coord

        # CW
        else:
            if (i == 0):
                ordered_contour_map[i] = coord
            else:
                ordered_contour_map[num_coords - i] = coord

    num_contours = len(ordered_contour_map)

    x1, y1 = ordered_contour_map[int(num_contours / 4)]
    x2, y2 = ordered_contour_map[int(num_contours / 2)]
    x3, y3 = ordered_contour_map[int(3 * num_contours / 4)]

    plt.scatter(x1,y1, c= "#FF0000")
    plt.text(x1,y1, "1")

    plt.scatter(x2,y2, c= "#18FF00")
    plt.text(x2,y2, "2")

    plt.scatter(x3,y3, c= "#8400FF")
    plt.text(x3,y3, "3")

    calc_ori = checkPolygon(ordered_contour_map)

    plt.text(10,10, calc_ori)

    #plt.show()

    url = (imgur_url.split("/"))[3]
    url = url.split(".")[0]

    name = url + "_" + str(orientation) + ".png"

    plt.savefig(str("shapes/" + name))

