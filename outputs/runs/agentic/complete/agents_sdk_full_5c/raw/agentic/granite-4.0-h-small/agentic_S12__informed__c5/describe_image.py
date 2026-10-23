import os
from vision_client import VisionClient
from vision_models import normalize_description

def describe_image(image_path):
    """Generates a concise visual description of a static image using Azure AI Vision.
    Returns a normalized description string.
    """
    client = VisionClient(service='vision')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.describe_image(Image={'Bytes': image_bytes})
    # Azure returns a list of captions; pick the highest confidence
    description = response.get('captions', [{}])[0].get('text', '')
    return normalize_description(description)
