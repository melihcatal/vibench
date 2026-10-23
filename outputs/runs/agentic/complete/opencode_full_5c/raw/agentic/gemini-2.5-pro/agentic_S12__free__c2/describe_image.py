import google.generativeai as genai
import os
from PIL import Image
import requests
from io import BytesIO
from vision_models import ImageDescription


def describe_image(image_uri: str) -> ImageDescription:
    """Generates a short visual description for an image using Google Gemini."""
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-pro-vision")

    response = requests.get(image_uri)
    img = Image.open(BytesIO(response.content))

    prompt_parts = [
        "Generate a short, descriptive alt text for this image.",
        img,
    ]

    output = model.generate_content(prompt_parts)
    return ImageDescription(text=output.text)
