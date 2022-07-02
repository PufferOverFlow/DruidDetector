import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import binary2image
import os
import glob
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import save_img

# File path
filepath = './models/dex/CNN_3.h5'

# Load the model
model = tf.keras.models.load_model(filepath, compile=True)


# Convert dex list to a image 420x220
def dex_to_image(dex_path):
    binary2image.main(dex_path)
    #return image_list

def predect_dex_based(dex_path):
    dex_to_image(r'temp_dex')
    img_path = os.path.join('dex_images', os.path.basename(dex_path)[:-4]+'_L.png')
    print(img_path)
    img = image.load_img(img_path, target_size=(420, 220))
    img_result = image.load_img(img_path, target_size=(1000, 600))
    img_array = image.img_to_array(img)
    img_array_result = image.img_to_array(img_result)
    save_img("static/dex_images/"+os.path.basename(dex_path)[:-4]+"_L.png", img_array_result)
    img_batch = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_batch)
    print(predictions)
    print(predictions.round())
    keras.backend.clear_session()
    return predictions,img_path


