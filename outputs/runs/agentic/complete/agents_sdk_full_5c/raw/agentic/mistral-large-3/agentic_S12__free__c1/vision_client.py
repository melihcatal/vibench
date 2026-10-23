import os
from google.cloud import vision_v1


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision API client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    return vision_v1.ImageAnnotatorClient()