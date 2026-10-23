import os
from typing import List, Dict

# Load credentials from environment (example for Google Cloud Vision)
# export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
assert GOOGLE_APPLICATION_CREDENTIALS, "Set GOOGLE_APPLICATION_CREDENTIALS env variable"

from google.cloud import vision_v1

client = vision_v1.ImageAnnotatorClient()

def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Return a singleton Vision API client."""
    return client
