import os
from typing import Optional, Dict, Any
from google.cloud import vision
from google.oauth2 import service_account


class VisionClient:
    """Local configuration and client helper utilities for Static Image and Visual Understanding."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Cloud Vision client.

        Args:
            credentials_path: Path to Google Cloud service account credentials JSON file.
                             If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        self.credentials_path = credentials_path
        self._client = None

    @property
    def client(self) -> vision.ImageAnnotatorClient:
        """Get or create Google Cloud Vision client."""
        if self._client is None:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = vision.ImageAnnotatorClient(credentials=credentials)
            else:
                self._client = vision.ImageAnnotatorClient()
        return self._client

    def load_image(self, image_path: str) -> vision.Image:
        """Load image from file path."""
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        return vision.Image(content=content)

    def validate_image_path(self, image_path: str) -> bool:
        """Validate that image file exists and is readable."""
        return os.path.exists(image_path) and os.path.isfile(image_path)

    @staticmethod
    def get_environment_config() -> Dict[str, str]:
        """Get configuration from environment variables."""
        config = {
            "google_application_credentials": os.environ.get(
                "GOOGLE_APPLICATION_CREDENTIALS"
            ),
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
        }
        return config
