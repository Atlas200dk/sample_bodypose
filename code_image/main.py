import os
import cv2
import numpy as np
import argparse
import sys
sys.path.append('..')
from model_processor import ModelProcessor
import acl
from acl_resource import AclResource

MODEL_PATH = "../model/body_pose.om"
DATA_PATH = './tennis_player.jpg'

def execute(model_path, frames_input_src, output_dir):
    

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
    # Read the image input using OpenCV
    img_original = cv2.imread(args.frames_input_src)

    ## Model Prediction ##
    # model_processor.predict: processing + model inference + postprocessing
    # canvas: the picture overlayed with human body joints and limbs
    canvas = model_processor.predict(img_original)

    # Save the detected results
    cv2.imwrite(os.path.join(args.output_dir, 'Result_Pose.jpg'), canvas)
    

if __name__ == '__main__':   
    description = 'Load a model for human pose estimation'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--model', type=str, default=MODEL_PATH)
    parser.add_argument('--frames_input_src', type=str,default=DATA_PATH, help="Directory path for image")
    parser.add_argument('--output_dir', type=str, default='./outputs', help="Output Path")

    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    execute(args.model, args.frames_input_src, args.output_dir)
