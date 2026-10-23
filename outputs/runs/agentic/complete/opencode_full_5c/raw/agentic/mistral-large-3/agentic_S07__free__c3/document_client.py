import os
from typing import Optional
from google.cloud import vision_v1
from google.oauth2 import service_account


def get_google_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initialize and return a Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    return vision_v1.ImageAnnotatorClient(credentials=credentials)


def normalize_bounding_box(vertices: list) -> dict:
    """Normalize bounding box vertices into a consistent format."""
    return {
        "vertices": [
            {"x": vertex.get("x", 0), "y": vertex.get("y", 0)} for vertex in vertices
        ]
    }
