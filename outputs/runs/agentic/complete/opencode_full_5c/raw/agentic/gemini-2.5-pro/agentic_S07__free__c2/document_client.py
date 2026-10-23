from google.cloud import vision
import os


def get_vision_client():
    """
    Initializes and returns a Google Cloud Vision API client.
    Assumes that GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return vision.ImageAnnotatorClient()
