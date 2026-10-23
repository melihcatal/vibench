import os
from google.cloud import vision


def get_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return vision.ImageAnnotatorClient()
