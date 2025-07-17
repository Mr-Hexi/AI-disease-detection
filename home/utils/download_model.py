# scans/utils/download_model.py
import os
import gdown

def download_model_if_needed():
    model_dir = "models"
    model_path = os.path.join(model_dir, "clf-resnet-weights.hdf5")

    if not os.path.exists(model_path):
        print("Model not found, downloading from Google Drive...")
        os.makedirs(model_dir, exist_ok=True)
        gdown.download(
            "https://drive.google.com/uc?id=1eRUeOkFi0vTEs4xAtstvLdoF2LFWCV52",
            model_path,
            quiet=False
        )
    else:
        print("Model already exists.")
