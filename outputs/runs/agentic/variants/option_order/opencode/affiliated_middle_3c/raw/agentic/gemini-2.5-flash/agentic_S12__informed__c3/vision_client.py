import os
from google.cloud import vision


def get_vision_client():
    """
    Returns a Google Cloud Vision client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    return vision.ImageAnnotatorClient()
