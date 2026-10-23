import os
from typing import Optional, Dict, Any
from google.cloud import vision


class VisionClient:
    """Client helper utilities for Static Image and Visual Understanding."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the vision client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                             If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = vision.ImageAnnotatorClient()

    def load_image(self, image_path: str) -> vision.Image:
        """Load image from file path."""
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        return vision.Image(content=content)

    def get_client(self) -> vision.ImageAnnotatorClient:
        """Get the Google Cloud Vision client instance."""
        return self.client

    @staticmethod
    def get_environment_config() -> Dict[str, str]:
        """Get environment configuration for vision services."""
        config = {
            "GOOGLE_APPLICATION_CREDENTIALS": os.getenv(
                "GOOGLE_APPLICATION_CREDENTIALS", ""
            ),
            "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT", ""),
            "VISION_API_ENDPOINT": os.getenv(
                "VISION_API_ENDPOINT", "https://vision.googleapis.com"
            ),
        }
        return config

    @staticmethod
    def validate_config() -> bool:
        """Validate that required environment variables are set."""
        required_vars = ["GOOGLE_APPLICATION_CREDENTIALS"]
        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            print(f"Missing required environment variables: {missing}")
            return False
        return True
