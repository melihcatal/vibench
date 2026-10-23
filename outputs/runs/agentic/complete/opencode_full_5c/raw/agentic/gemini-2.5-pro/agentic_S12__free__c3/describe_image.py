import google.generativeai as genai
import os
from vision_models import ImageDescription
from PIL import Image
import requests
from io import BytesIO

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def describe_image(image_uri: str) -> ImageDescription:
    """Generates a short visual description for an image using Google Gemini."""

    response = requests.get(image_uri)
    img = Image.open(BytesIO(response.content))

    model = genai.GenerativeModel("gemini-pro-vision")

    response = model.generate_content(["Describe this image in one sentence.", img])

    return ImageDescription(text=response.text)
