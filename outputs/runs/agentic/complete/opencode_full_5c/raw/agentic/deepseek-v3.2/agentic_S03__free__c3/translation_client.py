import os
from typing import Optional, Dict, Any
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account


class TranslationClient:
    """Client helper for Google Cloud Translation API."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize translation client.

        Args:
            credentials_path: Optional path to service account credentials JSON file.
                             If not provided, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = translate.Client(credentials=credentials)
        else:
            self.client = translate.Client()

    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages from Google Cloud Translation API."""
        results = self.client.get_languages()
        return {lang["language"]: lang["name"] for lang in results}

    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text using Google Cloud Translation API."""
        result = self.client.detect_language(text)
        return {
            "language": result["language"],
            "confidence": result.get("confidence", 0.0),
        }

    def get_client(self) -> translate.Client:
        """Get the underlying Google Cloud Translation client."""
        return self.client
