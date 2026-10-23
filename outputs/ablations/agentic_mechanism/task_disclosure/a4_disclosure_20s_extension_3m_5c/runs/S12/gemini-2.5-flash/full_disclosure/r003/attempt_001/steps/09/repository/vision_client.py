import os
from google.cloud import vision

def get_vision_client():
    """
    Provides a configured Google Cloud Vision API client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    or uses default credential discovery.
    """
    return vision.ImageAnnotatorClient()

