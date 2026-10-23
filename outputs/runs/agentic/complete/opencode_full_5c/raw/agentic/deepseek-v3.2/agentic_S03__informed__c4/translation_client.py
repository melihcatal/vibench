import os
from typing import Optional
from google.cloud import translate_v2 as translate


class TranslationClient:
    """Client helper for Google Cloud Translation API."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Cloud Translation client.

        Args:
            credentials_path: Optional path to service account credentials JSON file.
                             If not provided, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = translate.Client()

    def get_supported_languages(self) -> list[dict]:
        """Get list of supported languages from Google Cloud Translation."""
        return self.client.get_languages()

    def detect_language(self, text: str) -> dict:
        """Detect the language of given text."""
        return self.client.detect_language(text)

    def translate_with_details(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> dict:
        """Translate text with detailed response."""
        kwargs = {"target_language": target_language}
        if source_language:
            kwargs["source_language"] = source_language

        return self.client.translate(text, **kwargs)

    @staticmethod
    def validate_language_code(code: str) -> bool:
        """Validate if language code format is valid (basic check)."""
        return isinstance(code, str) and len(code) == 2

    @staticmethod
    def get_default_target_language() -> str:
        """Get default target language from environment or use Spanish."""
        return os.environ.get("DEFAULT_TARGET_LANGUAGE", "es")

    @staticmethod
    def get_default_source_language() -> str:
        """Get default source language from environment or use English."""
        return os.environ.get("DEFAULT_SOURCE_LANGUAGE", "en")
