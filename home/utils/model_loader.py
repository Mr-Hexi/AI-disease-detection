import os

from home.utils.download_model import download_model_if_needed
from home.brain_tumor import load_resnet  # assuming this builds your model

_model = None  # cache the model in memory

def get_model():
    global _model

    if _model is None:
        print("🔁 Model not loaded, loading now...")
        download_model_if_needed()

        model_path = os.path.join("models", "clf-resnet-weights.hdf5")
        _model = load_resnet(model_path)  # or load_model(model_path) if it's saved fully

    return _model
