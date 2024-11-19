import tensorflow.keras.models as models
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt
import io
import h5py

async def load_model(img_path):

    img = load_img(img_path, color_mode='grayscale', target_size=(124, 124))
    img_m = img_to_array(img)
    img_m = img_m / 255.0
    imagen_batch = np.expand_dims(img_m, axis=0)

    classes = ["glioma", "meningioma", "notumor", "pituitary"]
    model = await models.load_model('./models/model.h5')
    await model.load_weights('./models/checkpoint.weights.keras')
    predict = model.predict(imagen_batch)
    result = dict(zip(classes, predict[0]))
    
    return result
