from fastapi import FastAPI, UploadFile, File
import uvicorn 
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()
MODEL = tf.keras.models.load_model("../models/1.keras")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
  return "Hello, I'M LIVE"

def read_file_as_image(data) -> np.ndarray:
  return np.array(Image.open(BytesIO(data)))


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
  bytes = await file.read()
  image = read_file_as_image(bytes)
  img_batch = np.expand_dims(image, 0)
  predictions = MODEL.predict(img_batch)
  predict_class = CLASS_NAMES[np.argmax(predictions[0])]
  confidance = np.max(predictions[0])
  return{
    "class": predict_class,
    "confidenc": float(confidance)
  }

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8080)



  