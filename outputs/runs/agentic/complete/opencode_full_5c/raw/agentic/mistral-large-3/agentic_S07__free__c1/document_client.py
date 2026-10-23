import os
from typing import Optional
from google.cloud import vision_v1
from google.oauth2 import service_account


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initialize and return a Google Cloud Vision client."""
    credentials = None
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    return vision_v1.ImageAnnotatorClient(credentials=credentials)
