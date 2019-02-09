"""
General functions applied on image folder, such as:
1. copy folder
2. distribution query on steering angle
3. query folder size and image number
4. create header for log file if headless

Log
to be done [10/02/2019]
1. delete some rows with specified steering angle (keep the path of deleted files)
2. append augmented data on log file

input: path to folder containing logfile and image folder

remarks:
1. assume image folder name is 'IMG'
2. assume log file name is 'driving_log.csv'
3. check and convert path class in main
"""
import os
from pathlib import Path
from shutil import copy
import pandas as pd
import matplotlib.pyplot as plt

ORIG_LOG = 'driving_log.csv'
NEW_LOG = 'driving_log_new.csv'
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

def copy_logfile(file_path):
    """copy log file and named it as NEW_LOG, saved in the same folder
    if ther is existing log file named as NEW_LOG, ask user if it is to overwrite

    key arguments:
    file_path -- Path: path to log file csv (to be copied)
    """
    target_path = file_path.parents[0] / NEW_LOG
    if target_path.exists():
        is_rm = input('Overwrite existing log file? (y/n)')
        if is_rm == 'y':
            os.remove(str(target_path))
        elif is_rm == 'n':
            return None
        else:
            print('Invalid input!')
            return None
    copy(src = str(file_path), dst = str(target_path))
    print('Copy log file completed')
    print('[source path] ', file_path)
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
 
def add_header(file_path):
    """create header for log file if it is absent
    overwrite existing log file
    column order: center, left, right, steering, throttle, brake, speed 
    
    key arguments
    file_path -- Path: path to log file csv
    """
    df = pd.read_csv(file_path)
    if list(df)[0] != 'center':
        col_names = ['center', 'left', 'right', 'steering', 'throttle', 'brake', 'speed']
        df = pd.read_csv(file_path, names = col_names)
        df.to_csv(file_path, index = False)
        print('Created header for log file')
        print('[write path] ', file_path) 
    return df

def get_steering_dist(file_path, bins = 10):
    """plot the distribution of steering angle recorded in log file
    the function assumes there is a header in log file

    key arguments
    file_path -- Path: path to log file csv
    """
    df = pd.read_csv(file_path)
    plt.hist(df['steering'], bins = bins)
    print('Print out the distribution of steering angle...')
    print('[target path] ', file_path)
    plt.show()
    return None    

if __name__ == '__main__':
    parent_path = Path('/Users/hongyeah2151/Desktop/HKU/MDASC/2019_Sem2/Projects/donkey_car/sim_data')
    get_steering_dist(parent_path/NEW_LOG)
