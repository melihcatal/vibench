from google.cloud import vision
import os


def get_vision_client():
    """
    Initializes and returns a Google Cloud Vision API client.
    Authentication is handled automatically via the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.
    """
    return vision.ImageAnnotatorClient()
