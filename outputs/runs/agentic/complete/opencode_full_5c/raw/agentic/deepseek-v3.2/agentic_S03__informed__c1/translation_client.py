import os
from google.cloud import translate_v2 as translate
from typing import Optional, Dict, Any, List


class TranslationClient:
    """Local configuration and client helper utilities for Google Cloud Translation."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize the translation client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = translate.Client()

    def get_supported_languages(
        self, target_language: str = "en"
    ) -> List[Dict[str, Any]]:
        """Get list of supported languages from Google Cloud Translation."""
        results = self.client.get_languages(target_language=target_language)
        return [
            {"language": lang["language"], "name": lang["name"]} for lang in results
        ]

    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of a text string."""
        result = self.client.detect_language(text)
        return {
            "language": result["language"],
            "confidence": result.get("confidence", 0.0),
            "input": text,
        }

    def validate_language_code(self, language_code: str) -> bool:
        """Validate if a language code is supported."""
        try:
            languages = self.get_supported_languages()
            supported_codes = {lang["language"] for lang in languages}
            return language_code in supported_codes
        except Exception:
            return False

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
            "default_target_language": os.environ.get("DEFAULT_TARGET_LANGUAGE", "en"),
            "default_source_language": os.environ.get("DEFAULT_SOURCE_LANGUAGE"),
        }
