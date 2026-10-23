"""
translation_client.py - Provide local configuration and client helper utilities
for General Text Translation.

Provider: Google Cloud Translation (translate.googleapis.com)
SDK: google-cloud-translate
"""

import os
from typing import Optional

from google.cloud import translate_v2 as translate


GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

_translation_client: Optional[translate.Client] = None


def get_translation_client() -> translate.Client:
    """
    Get or create a singleton Google Cloud Translation client.

    Uses the google-cloud-translate SDK (v2) to create a client that connects
    to translate.googleapis.com.

    Returns:
        Configured google.cloud.translate_v2.Client instance.

    Raises:
        ValueError: If required configuration is missing.
    """
    global _translation_client

    if _translation_client is not None:
        return _translation_client

    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable is required "
            "for Google Cloud Translation API access."
        )

    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required "
            "for Google Cloud Translation API authentication."
        )

    _translation_client = translate.Client()
    return _translation_client


def reset_client() -> None:
    """Reset the global translation client (useful for testing)."""
    global _translation_client
    _translation_client = None


def get_supported_languages() -> list:
    """
    Get list of supported languages from Google Cloud Translation API.

    Returns:
        List of language codes supported by translate.googleapis.com.
    """
    client = get_translation_client()
    return client.get_languages()
