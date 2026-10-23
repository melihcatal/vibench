import os
from vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient()
    # Using Google Cloud Vision API with provider credentials from env vars
    response = client.label_detection(image_path)
    # Normalize response to list of detected labels
    return client.normalize_labels(response)
