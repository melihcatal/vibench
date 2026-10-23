import os
from typing import Optional
from google.cloud import vision
from google.oauth2 import service_account


def get_vision_client() -> Optional[vision.ImageAnnotatorClient]:
    """Initialize and return a Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        return None

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    return vision.ImageAnnotatorClient(credentials=credentials)