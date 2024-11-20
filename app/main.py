import io
import numpy as np
import tensorflow.keras.models as models
from fastapi import FastAPI, UploadFile
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = models.load_model('./app/models/model.h5')
model.load_weights('./app/models/checkpoint.weights.keras')

app = FastAPI()

@app.post("/process-image/")
async def predict_image(file: UploadFile):
    contents  = await file.read()
    img = io.BytesIO(contents)
    
    img = load_img(img, color_mode='grayscale', target_size=(124, 124))
    img_m = img_to_array(img)
    img_m = img_m / 255.0
    imagen_batch = np.expand_dims(img_m, axis=0)

    classes = ["glioma", "meningioma", "notumor", "pituitary"]
    predict = model.predict(imagen_batch)

    result = zip(classes, predict[0].tolist())

    return {"predict": result}