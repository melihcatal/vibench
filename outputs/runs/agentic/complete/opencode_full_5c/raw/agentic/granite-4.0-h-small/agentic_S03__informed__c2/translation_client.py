# [HELPER] translation_client.py

# Centralized configuration and client helpers for General Text Translation
import os
from typing import Any

# Choose one concrete provider per project (example: DeepL)
SERVICE = "DeepL"

# Mapping of service names to client constructors
CLIENT_CREATORS = {
    "DeepL": lambda key: DeepL(auth_key=key),
    # Add other providers here if needed
}

# Load auth key from environment variable
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

# Create a single shared client instance (singleton pattern)
_client = CLIENT_CREATORS[SERVICE](DEEPL_AUTH_KEY)


def get_client() -> Any:
    """Return the initialized translation client.","""
    return _client


# Utility to normalize language codes to provider format if needed


def normalize_lang(lang: str) -> str:
    """Map common language abbreviations to DeepL format.","""
    mapping = {
        "en": "EN",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "ja": "JA",
        # Extend as needed
    }
    return mapping.get(lang.lower(), lang.upper())
