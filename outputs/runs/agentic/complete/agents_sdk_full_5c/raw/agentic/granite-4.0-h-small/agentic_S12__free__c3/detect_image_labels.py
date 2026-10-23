import requests
from vision_client import VisionClient

def detect_image_labels(image_path):
    """Detect labels/objects in a static image using Google Cloud Vision API.
    Returns a list of detected label annotations.
    """
    client = VisionClient()
    image = client.load_image(image_path)
    response = client.annotate_image({"features": [{"type": "LABEL_DETECTION", "maxResults": 10}]})
    labels = response["labelAnnotations"]
    return [{"description": label["description"], "score": label["score"]} for label in labels]
