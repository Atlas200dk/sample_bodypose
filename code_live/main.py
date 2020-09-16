import random
import os
import cv2
import numpy as np
import argparse
import sys
sys.path.append('..')
from model_processor import ModelProcessor
from atlas_utils.camera import Camera
from atlas_utils import presenteragent
from atlas_utils.acl_image import AclImage
import acl
from acl_resource import AclResource

MODEL_PATH = "../model/body_pose.om"
BODYPOSE_CONF="../body_pose.conf"
CAMERA_FRAME_WIDTH = 1280
CAMERA_FRAME_HEIGHT = 720

def execute(model_path):

    ## Initialization ##
    #initialize acl runtime 
    acl_resource = AclResource()
    acl_resource.init()

    ## Prepare Model ##
    # parameters for model path and model inputs
    model_parameters = {
        'model_dir': model_path,
        'width': 368, # model input width      
        'height': 368, # model input height
    }
    # perpare model instance: init (loading model from file to memory)
    # model_processor: preprocessing + model inference + postprocessing
    model_processor = ModelProcessor(acl_resource, model_parameters)
    
    ## Get Input ##
    # Initialize Camera
    cap = Camera(id = 0, fps = 10)

    ## Set Output ##
    # open the presenter channel
    chan = presenteragent.presenter_channel.open_channel(BODYPOSE_CONF)
    if chan == None:
        print("Open presenter channel failed")
        return



    while True:
        ## Read one frame from Camera ## 
        img_original = cap.read()
        if not img_original:
            print('Error: Camera read failed')
            break
        # Camera Input (YUV) to RGB Image
        image_byte = img_original.tobytes()
        image_array = np.frombuffer(image_byte, dtype=np.uint8)
        img_original = YUVtoRGB(image_array)
        img_original = cv2.flip(img_original,1)

        ## Model Prediction ##
        # model_processor.predict: processing + model inference + postprocessing
        # canvas: the picture overlayed with human body joints and limbs
        canvas = model_processor.predict(img_original)
        
        ## Present Result ##
        # convert to jpeg image for presenter server display
        _,jpeg_image = cv2.imencode('.jpg',canvas)
        # construct AclImage object for presenter server
        jpeg_image = AclImage(jpeg_image, img_original.shape[0], img_original.shape[1], jpeg_image.size)
        # send to presenter server
        chan.send_detection_data(img_original.shape[0], img_original.shape[1], jpeg_image, [])

    # release the resources
    cap.release()

def YUVtoRGB(byteArray):
    e = 1280*720
    Y = byteArray[0:e]
    Y = np.reshape(Y, (720,1280))

    s = e
    V = byteArray[s::2]
    V = np.repeat(V, 2, 0)
    V = np.reshape(V, (360,1280))
    V = np.repeat(V, 2, 0)

    U = byteArray[s+1::2]
    U = np.repeat(U, 2, 0)
    U = np.reshape(U, (360,1280))
    U = np.repeat(U, 2, 0)

    RGBMatrix = (np.dstack([Y,U,V])).astype(np.uint8)
    RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2RGB, 3)
    return RGBMatrix
   

if __name__ == '__main__':   

    description = 'Load a model for human pose estimation'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--model', type=str, default=MODEL_PATH)
    args = parser.parse_args()

    execute(args.model)
