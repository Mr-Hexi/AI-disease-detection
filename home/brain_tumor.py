import cv2
import numpy as np
from skimage import io
from PIL import Image 
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50




        
def preprocess_img(img_path:str,mask:bool=False):
        img = io.imread(img_path)
        img = cv2.resize(img, (256,256))
        img = np.array(img, dtype=np.float64)
        if mask:
            img -= img.mean()
            img /= img.std()
        else:
            img = img *1./255.
        img = np.expand_dims(img,0)
        return img
    





 
    

    
