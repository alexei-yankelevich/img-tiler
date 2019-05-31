# author: alexyank@gmail.com
# date: 2019-05-27
# Tool for splitting big image into tiles of a predefined size
###################################################################

from sklearn.datasets import load_sample_image
from sklearn.feature_extraction import image

import cv2

import os
from os.path import splitext
from os import listdir
from os.path import isfile, join

def is_image_file(path):
    return isfile(path) and (path.lower().endswith(".png") or path.lower().endswith(".jpg"))

#here parameters of the splitter can be changed
source_img_dir = './'
tiles_dir = 'tiles'
tile_shape = (608,608,3)
# value just for sanity check that split makes sense
min_tile_number_per_dimention = 2

#check output tile directory and create if not exists
if not os.path.exists(tiles_dir):
    os.makedirs(tiles_dir)

#walk through all the files in the source image directory
img_files = [f for f in listdir(source_img_dir) if is_image_file(join(source_img_dir,f))]

#break each file into patches
for img_name in img_files:
    img_path = join(source_img_dir,img_name)
    img = cv2.imread(img_path)
    print('Processing: {}, Shape {}'.format(img_path,img.shape))
    if img.shape[0]<=tile_shape[0]*min_tile_number_per_dimention or img.shape[1] <= tile_shape[1]*min_tile_number_per_dimention:
        print('Seems like image {} is too small for splitting'.format(img_path))

    tile_rows = img.shape[0]/tile_shape[0]
    tile_cols = img.shape[1]/tile_shape[1]

    #get name and extension parts from file
    img_name_parts = splitext(img_name)

    for row in range(tile_rows):
        for col in range(tile_cols):
            # generate tile anme as <file_name_wo_ext>_<row>_<col>.jpg 
            tile_name = img_name_parts[0]+'_{}_{}.jpg'.format(row,col)
            tile = img[row*tile_shape[0]:(row+1)*tile_shape[0],col*tile_shape[1]:(col+1)*tile_shape[1],:]
            cv2.imwrite(join(tiles_dir,tile_name),tile)
    

