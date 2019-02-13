"""
Role:
Apply functions from img_folder.py and log_file.py on image processing pipeline

Functions:
1. to reduce the skewness of steering angle distribution, we flip those images with steering angle not equal to 0
2. we cut down some data with steering angle = 0

Remarks:
1. assume log file has headers

"""
import os
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
from img_folder import *
from log_file import *

def main():
    """ 
    put all actions in series: add headers, copy, delete rows, augment data
    """ 
    # set up arguments
    parser = argparse.ArgumentParser(description = 'Image Processing')
    parser.add_argument('-p', help = 'path to log file', dest = 'log_path', type = str, default = None)
    parser.add_argument('-c', help = 'copy or overwrite log file', dest = 'is_cp', type = int, default = 0) 
    parser.add_argument('-d', help = 'number of rows to be deleted', dest = 'rm_rows', type = int, default = 0)
    parser.add_argument('-e', help = 'change root path of image pointers', dest = 'img_root', type = str, default = None)
    parser.add_argument('-a', help = 'trigger for data augmentation', dest = 'is_aug', type = int, default = 0)
    args = parser.parse_args()
    
    # print out parameters
    print('-' * 30) 
    print('Parameters')
    print('-' * 30) 
    for key, value in vars(args).items():
        print('{:<20} := {}'.format(key, value))
    print('-' * 30) 
        
    log_path = Path(args.log_path)
    # decide if copy log file or not
    if args.is_cp:
        # copy log file and add headers
        log_path = respawn_log_copy(log_path)
        log_path = Path(log_path)
        print('[log_path] ', log_path)
    if args.rm_rows:
        delete_rows(log_path, rm_rows = args.rm_rows) 
    if args.img_root is not None:
        replace_root = Path(args.img_root)
        edit_log_path(log_path, replace_root)
    if args.is_aug:
        augment_run(log_path)
    pass


def augment_run(file_path):
    """read in log file, generate flipped image, appended the log file
    exclude rows with steering angle = 0

    key arguments:
    file_path -- Path: path to the log file
    """
    df = pd.read_csv(file_path)
    # only consider data with steering != 0
    filter_df = df[df.steering != 0]
    # create appended data 
    aug_data = gen_augment_data(filter_df)
    # transform list of dict into dataframe
    aug_data = syn_rows(aug_data)
    # appended data on log file
    append_rows(file_path, aug_data)
    print('Data augmentation completed')
    return None

def gen_augment_data(df):
    """iterate through a df and generate equal amt of flipped data
    generate flipped images, create pointer to the images, negate the steering angle
    output list of dict (they are the data of flipped images)
    assume the log file has headers

    key arguments:
    df -- DataFrame: dataframe to be iterated
    """
    aug_data = []
    for idx, row in df.iterrows():
        aug_row = gen_augment_row(row)
        aug_data.append(aug_row)
    return aug_data

def gen_augment_row(row):
    # original data info
    center_path = row['center']
    left_path = row['left']
    right_path = row['right']
    steering = row['steering']
    throttle = row['throttle']
    brake = row['brake']
    speed = row['speed']
    # augmented data info
    aug_row = {}
    # input Path instead of str
    aug_row['center'] = flip_img(Path(center_path))
    aug_row['left'] = flip_img(Path(left_path))
    aug_row['right'] = flip_img(Path(right_path))
    aug_row['steering'] = steering * -1
    aug_row['throttle'] = throttle
    aug_row['speed'] = speed
    return aug_row

def flip_img(in_path):
    """flip the image left and right and output the path to flipped image
    fixed format for the new image filename
    
    key arguments
    in_path -- Path: path to the image
    """
    im = Image.open(in_path)
    new_filename = in_path.stem + '_aug' + in_path.suffix
    out_path = in_path.parents[0]/new_filename
    im.transpose(Image.FLIP_LEFT_RIGHT).save(out_path)
    # output str instead of Path
    return str(out_path)

if __name__ == '__main__':
    main()
