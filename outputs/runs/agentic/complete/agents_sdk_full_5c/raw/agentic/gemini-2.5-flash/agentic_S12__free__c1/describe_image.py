import os
import google.generativeai as genai
from PIL import Image
import io

def describe_image(image_data: bytes, prompt: str = "Describe this image in a short sentence."):
    """Generates a short visual description for an image using Google's Gemini Pro Vision model."""
    # Ensure GOOGLE_API_KEY is set in your environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro-vision')

    image = Image.open(io.BytesIO(image_data))
    response = model.generate_content([prompt, image])
    return response.text

if __name__ == '__main__':
    # Example usage with a local image file
    # Replace with a path to a real image or fetch from a URL
    try:
        with open("example_image.jpg", "rb") as f:
            image_bytes = f.read()
        description = describe_image(image_bytes)
        print(f"Image Description: {description}")
    except FileNotFoundError:
        print("Please create an 'example_image.jpg' in the current directory for example usage.")
    except Exception as e:
        print(f"An error occurred: {e}")
