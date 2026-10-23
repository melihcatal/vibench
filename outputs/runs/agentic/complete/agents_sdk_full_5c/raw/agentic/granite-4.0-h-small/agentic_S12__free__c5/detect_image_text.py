import os
from vision_client import VisionClient

def detect_image_text(image_path):
    client = VisionClient()
    # Using Google Cloud Vision API with provider credentials from env vars
    response = client.text_detection(image_path)
    # Extract and clean recognized text strings
    texts = client.extract_text(response)
    return texts
