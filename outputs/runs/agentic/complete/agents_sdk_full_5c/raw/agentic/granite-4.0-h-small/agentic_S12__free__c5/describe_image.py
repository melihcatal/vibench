import os
from vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient()
    # Using Google Cloud Vision API with provider credentials from env vars
    response = client.image_ocr(image_path)
    # Return a short, human‑readable description
    description = client.summarize_description(response)
    return description
