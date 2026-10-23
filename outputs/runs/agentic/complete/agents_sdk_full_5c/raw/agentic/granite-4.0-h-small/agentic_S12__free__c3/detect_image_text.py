import requests
from vision_client import VisionClient

def detect_image_text(image_path):
    """Detect and extract any embedded text from an image using Google Cloud Vision OCR.
    Returns a list of extracted text blocks.
    """
    client = VisionClient()
    image = client.load_image(image_path)
    response = client.annotate_image({"features": [{"type": "TEXT_DETECTION", "maxResults": 10}]})
    texts = response.get("textAnnotations", [])
    return [text.get("description","") for text in texts]
