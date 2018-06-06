from glob import glob
import os
import cv2
from itertools import combinations

"""
収集した画像から重複する画像がないか調べる

"""

dir_list = os.listdir("../images")

images = glob("{dir}/*".format(dir=dir_list[0]))

image_hists = dict()
for image in images:
    img = cv2.imread()
    img = cv2.resize([100, 100])
    image_hists[image] = cv2.calcHist([img], [0], None, [256], [0, 256])

result = list()

for img_x, img_y in combinations(images, 2):
    pass
