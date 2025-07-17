import os
import cv2
import logging
import numpy as np
from PIL import Image 
from skimage import io
import tensorflow as tf
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"



def preprocess_img(img_path: str, mask: bool = False, resize_shape=(256, 256), normalize=True):
    img = io.imread(img_path)
    img = cv2.resize(img, resize_shape)
    img = np.array(img, dtype=np.float64)
    if normalize:
        img = img * 1.0 / 255.
    if mask:
        img -= img.mean()
        img /= img.std()
    img = np.expand_dims(img, 0)
    return img



def bt_predict(img_path, model, seg_model=None):
    # First predicting if there is Tumor or not
    img = preprocess_img(img_path=img_path, mask=False)
    clf_pred = model.predict(img)
    if clf_pred[0][0] < 0.5:
        print(" Please Provide Brain MRI SCAN")
    # else:
    # Second Masking the Area Where Tumor is Present
    if clf_pred.argmax() == 1:
    #     img = preprocess_img(img_path=img_path, mask=True)
    #     seg_predict = np.array(seg_model.predict(img)).squeeze().round()

    #     seg_img = io.imread(img_path)
    #     seg_img[seg_predict == 1] = (0, 255, 150)
        im = Image.open(img_path)
    #     im.save("media/bt_seg.jpg")
        im.save("media/bt.jpg")
        return 1,clf_pred.max()
    else:
        im = Image.open(img_path)
        im.save("media/no_bt.jpg")
        return 0, clf_pred.max()


    
    



