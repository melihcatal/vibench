import os
from typing import Optional, Dict, Any
import json


class TranslationClient:
    """Client helper utilities for Google Cloud Translation API."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize translation client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                             If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        self.credentials_path = credentials_path
        self._client = None

        # Set up credentials
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        elif "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set "
                "or credentials_path must be provided"
            )

    def get_client(self):
        """Get or create Google Cloud Translation client."""
        if self._client is None:
            from google.cloud import translate_v2 as translate

            self._client = translate.Client()
        return self._client

    def validate_language_code(self, lang_code: str) -> bool:
        """Validate if a language code is supported."""
        supported_codes = ["en", "es", "fr", "de", "zh", "ja", "ko", "ru", "ar", "hi"]
        return lang_code in supported_codes

    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and names."""
        client = self.get_client()
        results = client.get_languages()

        languages = {}
        for lang in results:
            languages[lang["language"]] = lang["name"]

        return languages

    def format_translation_request(
        self, text: str, source_lang: str, target_lang: str
    ) -> Dict[str, Any]:
        """Format translation request payload."""
        return {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
        }

    def parse_translation_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and normalize translation response."""
        return {
            "translated_text": response.get("translatedText", ""),
            "source_language": response.get("detectedSourceLanguage", ""),
            "original_text": response.get("input", ""),
            "model": "google-translation-api",
        }
