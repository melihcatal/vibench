import os
from google.cloud import vision


def get_vision_client():
    """
    Returns a Google Cloud Vision ImageAnnotatorClient.
    Relies on GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return vision.ImageAnnotatorClient()
