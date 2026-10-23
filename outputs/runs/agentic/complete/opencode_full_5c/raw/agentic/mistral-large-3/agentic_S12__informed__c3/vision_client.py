from google.cloud import vision_v1
from google.oauth2 import service_account
import os
from typing import Optional


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return vision_v1.ImageAnnotatorClient(credentials=credentials)
    else:
        return vision_v1.ImageAnnotatorClient()
