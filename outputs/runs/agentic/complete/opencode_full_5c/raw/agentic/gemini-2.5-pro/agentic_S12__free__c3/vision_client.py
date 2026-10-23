import os
from google.cloud import vision


def get_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()
