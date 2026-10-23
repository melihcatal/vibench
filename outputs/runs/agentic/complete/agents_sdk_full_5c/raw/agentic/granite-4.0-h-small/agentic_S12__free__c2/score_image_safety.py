import os
from vision_client import VisionClient

def score_image_safety(image_path):
    client = VisionClient()
    response = client.safe_image_content(image_path)  # Calls provider's unsafe content detection API
    # Assume response contains a confidence score and safe_flag
    return {
        'unsafe': response.unsafe,
        'confidence': response.confidence,
    }
