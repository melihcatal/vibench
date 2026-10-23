import os
from google.cloud import translate_v2 as translate
from typing import Optional, Dict, Any


class TranslationClient:
    """Local configuration and client helper utilities for Google Cloud Translation."""

    def __init__(
        self, project_id: Optional[str] = None, credentials_path: Optional[str] = None
    ):
        """Initialize Google Cloud Translation client with optional configuration."""
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        if project_id:
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

        self.client = translate.Client()

    def get_supported_languages(self) -> list[Dict[str, Any]]:
        """Get list of languages supported by Google Cloud Translation API."""
        return self.client.get_languages()

    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of given text."""
        return self.client.detect_language(text)

    def get_client_info(self) -> Dict[str, Any]:
        """Get information about the configured client."""
        return {
            "provider": "Google Cloud Translation API",
            "client_type": "translate_v2.Client",
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "Not set"),
            "credentials_set": "GOOGLE_APPLICATION_CREDENTIALS" in os.environ,
        }
