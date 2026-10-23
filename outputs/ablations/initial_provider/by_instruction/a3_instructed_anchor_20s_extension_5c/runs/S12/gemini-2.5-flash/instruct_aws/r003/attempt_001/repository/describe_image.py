import os
import google.generativeai as genai

def describe_image(image_bytes: bytes, model_name: str = "gemini-pro-vision") -> str:
    """
    Generates a short visual description for an image using Google Gemini Vision API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)
    image_part = {
        "mime_type": "image/jpeg",  # Assuming JPEG, can be made dynamic
        "data": image_bytes
    }
    response = model.generate_content(["Describe this image in detail.", image_part])
    return response.text
