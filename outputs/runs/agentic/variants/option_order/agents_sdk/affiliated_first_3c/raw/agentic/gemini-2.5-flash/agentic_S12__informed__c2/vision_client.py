import os
from google.cloud import vision

def get_vision_client() -> vision.ImageAnnotatorClient:
    """Returns a Google Cloud Vision API client instance."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    return vision.ImageAnnotatorClient()
