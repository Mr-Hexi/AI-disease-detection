import os
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

_model = None  # cache the model in memory

def get_model():
    global _model

    if _model is None:
        # model_path = os.path.join("models", "quantized_resnet_bt.h5")
        model_path = os.path.join("models", "brain_tumor_model_vgg16_99_val_acc_94_test_acc.h5")
        _model = tf.keras.models.load_model(model_path,compile=False)

    return _model
