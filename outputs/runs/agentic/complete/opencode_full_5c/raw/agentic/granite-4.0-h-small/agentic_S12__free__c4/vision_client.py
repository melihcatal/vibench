# vision_client.py
# LOCAL HELPER - Static Image and Visual Understanding

import os
from google.cloud import vision_v1

# Provider identification (Google Cloud Vision API)
PROVIDER = "Google Cloud Vision"


def get_client():
    """Create and return a Vision API client.
    Uses the GOOGLE_APPLICATION_CREDENTIALS environment variable for auth.
    """
    # Ensure the credentials file is set
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point to a service account json"
        )
    client = vision_v1.ImageAnnotatorClient()
    return client


def load_image_bytes(path):
    """Read an image file and return its bytes.
    Args:
        path (str): Local filesystem path to the image.
    Returns:
        bytes: Image content.
    """
    with open(path, "rb") as f:
        return f.read()
