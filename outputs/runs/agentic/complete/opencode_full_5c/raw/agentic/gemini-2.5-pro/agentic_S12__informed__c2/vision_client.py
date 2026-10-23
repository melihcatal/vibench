import os
from google.cloud import vision


def get_vision_client():
    """Initializes and returns a Google Cloud Vision API client."""

    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    client = vision.ImageAnnotatorClient()
    return client
