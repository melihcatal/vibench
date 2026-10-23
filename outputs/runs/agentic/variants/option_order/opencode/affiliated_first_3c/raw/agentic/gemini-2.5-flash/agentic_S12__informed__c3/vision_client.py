import os
from google.cloud import vision


def get_vision_client():
    # Google Cloud Vision client initialization
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return vision.ImageAnnotatorClient()
