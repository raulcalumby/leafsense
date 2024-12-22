import streamlit as st
import requests
from PIL import Image
import io

st.title("Potato Disease Classification")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

api_url = "http://localhost:8000/predict"  # FastAPI endpoint

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image.", use_container_width=True)

    if st.button("Analyze Health"):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format)
        img_bytes = img_bytes.getvalue()

        files = {"file": (uploaded_file.name, img_bytes, uploaded_file.type)}
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Result: {result['class']}")
        else:
            st.error("Error processing the image.")