import os
from vision_client import VisionClient

def score_image_safety(image_path):
    client = VisionClient()
    # Using Google Cloud Vision API with provider credentials from env vars
    response = client.safe_search_detection(image_path)
    # Normalize unsafe categories to a score (0-1)
    return client.normalize_safety_score(response)
