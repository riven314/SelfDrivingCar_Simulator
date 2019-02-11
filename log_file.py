"""
General functions applied on log file, such as:
1. distribution query on steering angle
2. create header for log file if headless
3. copy log file

to be done:
1. deleted some rows with specified steering angle (keep the path of deleted files)
2. appended augmented data on log file
3. change path for log file

remarks:
1. assume log file name is 'driving_log.csv'
2. check and convert path class in main

"""
import os
from pathlib import Path
from shutil import copy
import pandas as pd
import matplotlib.pyplot as plt

NEW_LOG = 'driving_log_new.csv'
ORIG_LOG = 'driving_log.csv'

def delete_rows(file_path, rm_steering = 0, rm_rows = 1000):
    """delete rows with specified steering angle in log file
    randomly pick rm_rows of rows for deletion
    assume the log file has headers

    key arguments:
    file_path -- Path: path to log file csv
    rm_steering -- double: steering angle where the deleted rows have
    rm_rows -- int: number of rows to be deleted
    """
    df = pd.read_csv(file_path)
    idxs = df[df.steering == rm_steering].sample(rm_rows).index
    df = df.drop(idxs)
    df.reset_index(drop = True, inplace = True)
    df.to_csv(file_path, index = False)
    print('Some rows in log file is deleted')
    print('[source path] ', file_path)
    print('[target_steering]: %d' % rm_steering)
    print('[rm_rows]: %d' % rm_rows)
    return None

def syn_rows(dict_ls):
    """concatenate a list of dict into a DataFrame
    it serves as rows appending
    
    key arguments:
    dict_ls -- list: list of dict with columns as key
    """
    rows_df = pd.DataFrame(dict_ls)
    return rows_df

def append_rows(file_path, rows_df):
    """append rows at the bottom of log file
    assume log file has headers

    key arguments
    file_path -- Path: path to log file csv
    rows_df -- DataFrame: rows to be appended
    """
    df = pd.read_csv(file_path)
    old_nrows = df.shape[0]
    df.append(rows_df).reset_index(drop = True, inplace = True)
    new_nrows = df.shape[0]
    print('Log file appended with rows')
    print('[source path] ', file_path)
    print('[number of new rows] %d' % (new_rows - old_rows))
    return df

def replace_path(orig_path, update_root):
    """replace the root path of orig_path by update_root
    
    key arguments
    orig_path -- Path: original path
    update_root -- Path: root path for replacement
    """
    filename = orig_path.name
    new_path = update_root/filename
    return new_path

def edit_log_path(file_path, update_root):
    """update the path in columns center, left and right
    assume headers exist and they are center, left and right

    key arguments
    file_path -- Path: path to log file csv
    update_path -- Path: path to be amended on log file
    """
    orig_root = file_path.parents[0]
    df = pd.read_csv(file_path)
    df.center = df.center.apply(lambda x: replace_path(Path(x), update_root))
    df.right = df.right.apply(lambda x: replace_path(Path(x), update_root))
    df.left = df.left.apply(lambda x: replace_path(Path(x), update_root))
    df.to_csv(file_path, index = False)
    print('Image pointer changed')
    print('[original root] ', orig_root)
    print('[updated root] ', update_root)
    return None

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

def create_header(file_path):
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

def respawn_log_copy(file_path):
    copy_logfile(file_path)
    new_path = p.parents[0]/NEW_LOG
    create_header(new_path)
    return None

if __name__ == '__main__':
    parent_path = Path('/Users/hongyeah2151/Desktop/HKU/MDASC/2019_Sem2/Projects/donkey_car/sim_data')
    p = parent_path/ORIG_LOG
    respawn_log_copy(p)
