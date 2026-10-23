from google.cloud import vision
import os

def get_vision_client():
    """
    Provides a Google Cloud Vision AI client.

    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    for authentication.
    """
    return vision.ImageAnnotatorClient()

