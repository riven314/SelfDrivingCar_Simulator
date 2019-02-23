"""
Helper functions used in drive.py

functions:
1. load in pretrained model weight
2. give prediction from an image path
3. give prediction from PIL class

"""
from fastai import *
from fastai.vision import *
import numpy as np
import pandas as pd
from pathlib import Path
import PIL

def load_model(data_path, model_path):
    """load in pretrained model weight

    key arguments
    data_path -- Path: path to data (for exporting past data for backup)
    model_path -- Path: path to the model (exclude suffix)
    """
    empty_data = ImageDataBunch.load_empty(data_path)
    learn = create_cnn(empty_data, models.resnet34, metrics = mean_squared_error)
    learn = learn.load(model_path)
    return learn

def predict_from_path(img_path, learn):
    """give prediction from an image path

    key arguments
    img_path -- Path: path to a new image
    learn -- Learner
    """
    img = open_image(img_path)
    # retrieve float from FloatItem
    pred = learn.predict(img)[0].obj[0]
    return pred

def predict_from_pil2(pil_img, learn):
    """give prediction from PIL object

    key arguments
    pil_img -- PIL2 object: image to be predicted
    learn -- Learner
    """
    img = pil_img.convert('RGB')
    img = pil2tensor(img, dtype = np.float32)
    # normalize the tensor
    img.div_(255)
    # convert from tensor to Image class
    img = Image(img)
    pred = learn.predict(img)[0].obj[0]
    return pred


