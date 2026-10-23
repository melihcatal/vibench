import os
from vision_client import VisionClient
from vision_models import normalize_labels

def detect_image_labels(image_path):
    """Detects objects/labels in a static image using AWS Rekognition.
    Returns a list of normalized label dictionaries.
    """
    client = VisionClient(service='rekognition')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_labels(Image={'Bytes': image_bytes})
    labels = [
        {"name": label['Name'], "confidence": label['Confidence']}
        for label in response.get('Labels', [])
    ]
    return normalize_labels(labels)
