import os

from vision_client import VisionClient
from vision_models import normalize_description

def describe_image(image_path: str) -> str:
    """Generate a short textual description of a static image using Amazon Rekognition.

    Returns a concise caption string.
    """
    client = VisionClient(service='rekognition')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.describe_image(Image={'Bytes': image_bytes})
    # SDK returns an array of captions; we take the first one
    caption = response.get('Captions', [{}])[0].get('Caption', '')
    return caption.strip()
