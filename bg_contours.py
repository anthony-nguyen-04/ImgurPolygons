import matplotlib.pyplot as plt
from skimage.segmentation import (morphological_chan_vese,
                                  checkerboard_level_set)
from bg_map import *
from skimage.io import imread
from pandas import DataFrame
from PolygonChecker import checkPolygon
import random

# 0 is CW, 1 is CCW
initial_orientation = random.randint(0,1)

# Morphological ACWE
input_file = ".\images\star.png"
#input_file = "https://i.imgur.com/XyUC9tj.jpg"

img = imread(input_file)

map = get_bg_map(img)

map = np.where(map > 0.5, 1, 0).astype(np.float32)


# Initial level set
init_ls = checkerboard_level_set(map.shape, 6)

# List with intermediate results for plotting the evolution
ls = morphological_chan_vese(map, num_iter=35, init_level_set=init_ls,
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

# print(len(int_contour))
# print(len(np.unique(int_contour, axis = 0)))


# x,y = biggest_contour_vertices.T
# x,y = int_contour.T
# plt.scatter(x[0],y[0])
# plt.scatter(x[500],y[500])
# plt.scatter(x[1000],y[1000])
# plt.scatter(x[1500],y[1500])

#plt.gca().invert_yaxis()

#plt.show()

#ordered_contour = enumerate(list(dict.fromkeys(map(tuple, int_contour))))
#ordered_contour = enumerate(pd.unique(int_contour))
ordered_contour = enumerate(DataFrame(int_contour).drop_duplicates().values)
ordered_contour = list(ordered_contour)

ordered_contour_map = {}
num_coords = len(ordered_contour)

for i, coord in ordered_contour:
    #ordered_contour_map[i] = coord

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
plt.scatter(x2,y2, c= "#18FF00")
plt.scatter(x3,y3, c= "#8400FF")

calc_ori = checkPolygon(ordered_contour_map)

plt.text(10,10, calc_ori)

plt.show()


#
# labels = (measure.label(ls)).transpose()
# def extract_blobs_from_labelled_array(labelled_array):
#     """Return a list containing coordinates of pixels in each blob."""
#     props = measure.regionprops(labelled_array)
#     blobs = [p.coords for p in props]
#     return blobs
#
# coords = extract_blobs_from_labelled_array(labels)[0]
# out = np.zeros(map.shape, np.uint8)
# cv2.drawContours(out, [coords], -1, 255, cv2.FILLED)
#
# out = cv2.bitwise_and(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), out)
#
# cv2.imshow('out', out)
# cv2.waitKey(0)
#
# #TODO
