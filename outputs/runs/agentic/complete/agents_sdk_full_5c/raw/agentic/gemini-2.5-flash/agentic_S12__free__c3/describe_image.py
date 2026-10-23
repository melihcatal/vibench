import os
import base64
from io import BytesIO
import google.generativeai as genai
from PIL import Image

def describe_image_from_bytes(image_bytes: bytes) -> str:
    """Generates a short visual description for an image given its bytes."""
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(BytesIO(image_bytes))
    response = model.generate_content(["Describe this image in a concise way.", img])
    return response.text


def describe_image_from_path(image_path: str) -> str:
    """Generates a short visual description for an image given its file path."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return describe_image_from_bytes(image_bytes)

if __name__ == '__main__':
    # Placeholder for actual usage.
    # For local testing, ensure you have a local image file and GEMINI_API_KEY set.
    # Example usage with a dummy image file (create a dummy image for testing)
    dummy_image_path = "dummy_image.jpg" # Replace with an actual image path for testing
    # Create a small dummy image for demonstration if it doesn't exist
    if not os.path.exists(dummy_image_path):
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (60, 30), color = 'red')
        d = ImageDraw.Draw(img)
        d.text((10,10), "Hello", fill=(255,255,0))
        img.save(dummy_image_path)
        print(f"Created a dummy image: {dummy_image_path}")

    try:
        print(f"Describing image: {dummy_image_path}")
        description = describe_image_from_path(dummy_image_path)
        print(f"Description: {description}")
    except Exception as e:
        print(f"Error describing image: {e}")
        print("Please ensure GEMINI_API_KEY is set and the image path is valid.")
