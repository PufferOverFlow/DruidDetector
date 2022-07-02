import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

# File path
filepath = './models/permission/CNNm4.h5'

# Load the model
model = tf.keras.models.load_model(filepath, compile=True)


# Convert permission list to a image 8*9
def permissions_to_image(dataset):
    #print(dataset)
    feature_len = len(dataset.columns)
    w = 9  # width=9

    apk_dt = np.array(dataset)
    image_list = []

    for row in range(0, len(dataset)):
        l = []
        for i in range(0, feature_len, w):
            l.append(list(apk_dt[row, i:i + w]))

        l[-1] = l[-1] + [0] * (w - len(l[-1]))
        img = Image.fromarray(np.array(l, dtype='int8'),
                              "L")  # Convert to grayscale image (because it is faster to run the model with 0,1, so directly use 0,1 to convert it into image form)
        image_list.append(img)

    return image_list


def predect_permission_based(permissions_list):
    # Convert Permissions to PIL image
    image_list = permissions_to_image(permissions_list)

    # Convert PIL image to numpy array, and then convert each numpy array to list
    img_array = [list(tf.keras.preprocessing.image.img_to_array(img)) for img in image_list]
    np_array = np.asarray(img_array)

    # Generate predictions for samples
    predictions = model.predict(np_array)
    #print(predictions)
    #print(y)
    #onehot_label = keras.utils.to_categorical(y)
    #results = model.evaluate(np_array,onehot_label)
    #print("test loss, test acc:", results)
    #score = model.predict(np_array).round()
    keras.backend.clear_session()

    return predictions
