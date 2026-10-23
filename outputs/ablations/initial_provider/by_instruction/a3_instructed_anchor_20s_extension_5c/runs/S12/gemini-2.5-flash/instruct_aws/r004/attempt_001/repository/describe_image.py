import os
import io
from typing import Dict, Any
import google.generativeai as genai
from PIL import Image

def describe_image(image_bytes: bytes) -> Dict[str, str]:
    """
    Generates a short visual description for an image using Google's Gemini Pro Vision model.

    Args:
        image_bytes: The image content as bytes.

    Returns:
        A dictionary containing the generated description.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(io.BytesIO(image_bytes))
    
    # Generate content with the image
    response = model.generate_content(["Describe this image in a concise way.", img])
    
    return {"description": response.text}
