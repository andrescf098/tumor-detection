from fastapi import FastAPI, File, HTTPException, UploadFile
from typing import Annotated
from app.utils.load_model import load_model
from PIL import Image
import io
import numpy as np

app = FastAPI()

@app.post("/process-image/")
async def predict_image(file: UploadFile):
    contents  = await file.read()
    img = io.BytesIO(contents)
    result = await load_model(img)
    return result