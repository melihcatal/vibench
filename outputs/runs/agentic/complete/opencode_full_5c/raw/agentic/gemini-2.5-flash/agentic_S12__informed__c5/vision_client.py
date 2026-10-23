import os
from google.cloud import vision


def get_vision_client():
    """
    Provides a Google Cloud Vision client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is the identifying signal.
    return vision.ImageAnnotatorClient()
