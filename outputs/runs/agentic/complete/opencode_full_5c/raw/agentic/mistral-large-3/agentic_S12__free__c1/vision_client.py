import os
from google.cloud import vision_v1
from google.cloud.storage import Client as StorageClient
from typing import Optional


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision API client."""
    return vision_v1.ImageAnnotatorClient()


def get_storage_client() -> Optional[StorageClient]:
    """Initializes and returns a Google Cloud Storage client if credentials are available."""
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return StorageClient()
    return None
