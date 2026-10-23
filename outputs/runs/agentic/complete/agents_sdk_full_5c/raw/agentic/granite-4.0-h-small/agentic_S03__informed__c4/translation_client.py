import os
import json
from typing import Mapping, Any
from translate_client import TranslationClient

class TranslationConfig:
    """Configuration for the translation client using a concrete provider."""

    SERVICE = "google-cloud-translate"  # concrete provider identifier
    SERVICE_URL = os.getenv(
        "TRANSLATION_SERVICE_URL", "https://translation.googleapis.com"
    )

    @staticmethod
    def get_client() -> TranslationClient:
        """Return a configured TranslationClient instance."""
        return TranslationClient()

    @classmethod
    def translate(cls, text: str, source_lang: str, target_lang: str) -> str:
        """Simple wrapper that mirrors the helper module usage."""
        client = cls.get_client()
        return client.translate(text, source_lang, target_lang)

def load_credentials() -> Mapping[str, Any]:
    """Load provider-specific credentials from environment variables."""
    return {
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", None
        )
    }

if __name__ == "__main__":
    # Example usage (remove or comment out for production)
    sample = "Hello, world!"
    result = TranslationConfig.translate(sample, "en", "es")
    print(f"Translated: {result}")
