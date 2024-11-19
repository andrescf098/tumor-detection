import tensorflow.keras.models as models
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np



def load_model():

    img = load_img('./files/Brain Tumor MRI/Prediction check images/no_tumor.jpg', color_mode='grayscale' ,target_size=(124, 124))
    img_m = img_to_array(img)
    img_m = img_m / 255.0
    imagen_batch = np.expand_dims(img_m, axis=0)
    classes = ["glioma", "meningioma", "notumor", "pituitary"]
    model = models.load_model('./models/model.h5')
    model.load_weights('./models/checkpoint.weights.keras')
    predict = model.predict(imagen_batch)
    result = dict(zip(classes, predict[0]))
    
    return print(result)


if __name__ == "__main__":
    load_model()