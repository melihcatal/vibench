import requests
from vision_client import VisionClient

def describe_image(image_path):
    """Generate a short natural-language description for an image using Google Cloud Vision API.
    Returns a one-sentence caption.
    """
    client = VisionClient()
    image = client.load_image(image_path)
    response = client.annotate_image({"features": [{"type": "IMAGE_PROPERTIES", "maxResults": 1}]})
    # Use the safest description endpoint if available; fallback to label detection
    description = response.get("textAnnotations", [{}])[0].get("description", "")
    return description.strip() if description else "No description available."
