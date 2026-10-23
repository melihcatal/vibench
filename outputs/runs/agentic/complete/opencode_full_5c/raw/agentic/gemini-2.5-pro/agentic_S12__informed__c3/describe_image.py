import os
import google.generativeai as genai
from PIL import Image


def describe_image(image_path: str) -> str:
    """
    Generates a short visual description for an image using Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    img = Image.open(image_path)

    prompt = "Provide a short, one-sentence description of this image."

    response = model.generate_content([prompt, img])

    return response.text
