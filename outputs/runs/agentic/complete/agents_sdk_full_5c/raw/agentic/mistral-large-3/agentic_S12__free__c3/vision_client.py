import os
from google.cloud import vision_v1

def get_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    return vision_v1.ImageAnnotatorClient()