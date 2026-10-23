"""Local configuration and client helper utilities for Static Image and Visual Understanding.

Uses Google Cloud Vision as the concrete provider.
Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
from typing import Optional

from google.cloud import vision as google_vision
from google.oauth2 import service_account


def get_google_application_credentials_path() -> str:
    """Return the path to the Google service account credentials file."""
    creds_path = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "gcp-vision-credentials.json",
    )
    return creds_path


def create_vision_client(
    credentials_path: Optional[str] = None,
) -> google_vision.ImageAnnotatorClient:
    """Create and return a configured Google Cloud Vision ImageAnnotatorClient.

    Args:
        credentials_path: Optional explicit path to a GCP service-account JSON key file.
            Falls back to GOOGLE_APPLICATION_CREDENTIALS env var if not provided.

    Returns:
        An authenticated google.cloud.vision.ImageAnnotatorClient instance.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return google_vision.ImageAnnotatorClient(credentials=credentials)

    default_creds = get_google_application_credentials_path()
    if os.path.isfile(default_creds):
        credentials = service_account.Credentials.from_service_account_file(
            default_creds
        )
        return google_vision.ImageAnnotatorClient(credentials=credentials)

    return google_vision.ImageAnnotatorClient()


def load_image_from_file(image_path: str) -> google_vision.Image:
    """Load a local image file into a google.cloud.vision.Image object.

    Args:
        image_path: Path to a local image file (JPEG, PNG, WEBP, GIF, etc.).

    Returns:
        A google.cloud.vision.Image instance with the file content set.
    """
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    return google_vision.Image(content=content)


def load_image_from_uri(image_uri: str) -> google_vision.Image:
    """Reference a remote image via URI for Google Cloud Vision.

    Args:
        image_uri: A gs://, http://, or https:// URI pointing to an image.

    Returns:
        A google.cloud.vision.Image instance with the image source URI set.
    """
    image = google_vision.Image()
    image.source.image_uri = image_uri
    return image


VISON_API_ENDPOINT = "vision.googleapis.com"
GOOGLE_VISION_MODEL_FAMILIES = {
    "label_detection": "builtin/stable",
    "text_detection": "builtin/stable",
    "image_properties": "builtin/stable",
    "safe_search": "builtin/stable",
    "face_detection": "builtin/stable",
    "landmark_detection": "builtin/stable",
    "logo_detection": "builtin/stable",
    "object_localization": "builtin/stable",
    "web_detection": "builtin/stable",
}
