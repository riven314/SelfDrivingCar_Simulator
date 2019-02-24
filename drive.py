import argparse
import base64
from datetime import datetime
import os
import shutil

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import PIL
from flask import Flask
from io import BytesIO

from pathlib import Path
from drive_util import *

sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

MAX_SPEED = 23
MIN_SPEED = 18

speed_limit = MAX_SPEED

# Cycle: send_control > sio_emit > data > telemetry
# data is from sio.emit(), send_control()
@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        # The current steering angle of the car
        steering_angle = float(data["steering_angle"])
        # The current throttle of the car
        throttle = float(data["throttle"])
        # The current speed of the car
        speed = float(data["speed"])
        # The current image from the center camera of the car
        image = PIL.Image.open(BytesIO(base64.b64decode(data["image"])))
        # save frame
        if args.image_folder != '':
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            image_filename = os.path.join(args.image_folder, timestamp)
            image.save('{}.jpg'.format(image_filename))

        try:
            #image = np.asarray(image)       # from PIL image to numpy array
            # resize, crop and change to other color channel
            #image = utils.preprocess(image) # apply the preprocessing
            #image = np.array([image])       # the model expects 4D array

            # predict the steering angle for the image
            steering_angle = float(predict_from_pil2(image, model))
            # lower the throttle as the speed increases
            # if the speed is above the current speed limit, we are on a downhill.
            # make sure we slow down first and then go back to the original max speed.
			
            # throttle pos: accelerate up to max speed (30)
            # throttle neg: deccelerate and move backwards 
            global speed_limit
            if speed > MAX_SPEED:
                throttle = -0.2  # slow down
            elif speed <= MAX_SPEED and speed >= MIN_SPEED:
                throttle = 0.1
            else:
                throttle = 0.2
            #throttle = 1.0 - steering_angle**2 - (speed/speed_limit)**2
			
            print('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle)
        except Exception as e:
            print(e)

    else:
        # NOTE: DON'T EDIT THIS.
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)

# throttle, steering_angle, brake, inset_image1, inset_image2 
def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        '-m',
        dest = 'model',
        type=str,
        help='Path to model file(exclude suffix)'
    )
    parser.add_argument(
        '-d',
        dest = 'data',
        type=str,
        help = 'Path to data folder'

    )
    parser.add_argument(
        '-i',
        dest = 'image_folder',
        type=str,
        default='',
        help='Path to image folder. This is where the images from the run will be saved.'
    )
    args = parser.parse_args()
    data_path = Path(args.data)
    model_path = Path(args.model)

    model = load_model(data_path, model_path)

    if args.image_folder != '':
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")
    else:
        print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
