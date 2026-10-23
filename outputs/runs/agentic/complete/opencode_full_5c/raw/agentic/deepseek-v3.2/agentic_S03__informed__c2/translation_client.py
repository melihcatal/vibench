from google.cloud import translate_v2 as translate
import os
from typing import Optional, List, Dict, Any


class TranslationClient:
    """Client helper for Google Cloud Translation operations."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the translation client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                             If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = translate.Client()

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of a text.

        Args:
            text: Text to detect language for

        Returns:
            Dictionary with language detection results
        """
        return self.client.detect_language(text)

    def get_supported_languages(
        self, target_language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Get list of supported languages.

        Args:
            target_language: Language to return language names in

        Returns:
            List of supported languages with codes and names
        """
        return self.client.get_languages(target_language=target_language)

    def validate_language_code(self, language_code: str) -> bool:
        """
        Validate if a language code is supported.

        Args:
            language_code: Language code to validate

        Returns:
            True if language is supported, False otherwise
        """
        try:
            languages = self.get_supported_languages()
            return any(lang["language"] == language_code for lang in languages)
        except Exception:
            return False

    @staticmethod
    def load_config_from_env() -> Dict[str, str]:
        """
        Load configuration from environment variables.

        Returns:
            Dictionary with configuration values
        """
        config = {
            "google_application_credentials": os.environ.get(
                "GOOGLE_APPLICATION_CREDENTIALS"
            ),
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
        }
        return config
