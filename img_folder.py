"""
General functions applied on image folder, such as:
1. query folder size and image number

to be done [10/02/2019]
1. add image in image folder
2. copy image to another image folder

remarks:
1. assume image folder name is 'IMG'
2. check and convert path class in main
"""
import os
from pathlib import Path
from shutil import copy, copytree
import pandas as pd
import matplotlib.pyplot as plt

NEW_IMG_FOLDER = 'IMG_NEW'
IMG_FOLDER = 'IMG'

def query_folder(folder_path):
    """print out no. of files and folder size.

    key arguments:
    folder_path -- Path: folder containing the images
    """
    # init
    img_num, folder_size = 0, 0
    byte2mb = 1e-6
    # pathlib available in python3
    if not folder_path.exists():
        print('Invalid path')
        return None
    for f in folder_path.iterdir():
        if f.suffix == '.jpg':
            img_num += 1
            folder_size += f.stat().st_size * byte2mb
    print('[Query path] ', folder_path)
    print('[folder size] {0:.{1}f} MB'.format(folder_size, 3))
    print('[image number] %d (.jpg)' % img_num)
    return None

def copy_imgfolder(folder_path):
    """ copy all images in original folder to new one called IMG_NEW
    assume IMG_NEW does not exist

    key arguments:
    folder_path -- Path: path to original image folder
    """
    target_path = folder_path.parents[0]/NEW_IMG_FOLDER
    # terminate if IMG_NEW exists
    if target_path.exists():
        print('Delete IMG_NEW before the execution')
        return None
    copytree(src = str(folder_path), dst = str(target_path))
    print('Copy image folder completed')
    print('[source path] ', folder_path)
    print('[target path] ', target_path)
    return None 

def unify_path(path_obj):
    """check convert path input as a Path class (introduced in python3)
    
    key arguments:
    path_obj -- str/Path: path to be examined
    """
    if not isinstance(path_obj, Path):
        path_obj = Path(path_obj)
    return path_obj
 

if __name__ == '__main__':
    p = '/Users/hongyeah2151/Desktop/HKU/MDASC/2019_Sem2/Projects/donkey_car/sim_data/IMG'
    p = unify_path(p)
    copy_imgfolder(p)
