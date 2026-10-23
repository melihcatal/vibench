from google.cloud import vision
import os

_vision_client = None

def get_vision_client():
    """
    Returns a singleton Google Cloud Vision AI client.
    Authenticates using Application Default Credentials.
    Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    or gcloud is configured.
    """
    global _vision_client
    if _vision_client is None:
        _vision_client = vision.ImageAnnotatorClient()
    return _vision_client
