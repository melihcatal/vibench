"""Local configuration and client helper utilities for General Text Translation."""

import os
from typing import Dict, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"

# Load credentials / configuration from environment
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError(
        f"{PROVIDER_NAME} requires {GOOGLE_APPLICATION_CREDENTIALS} env var"
    )


def build_client() -> Any:
    """Instantiate and return the provider SDK client.
    Returns:
        Initialized client object.
    """
    from google.cloud import translate_v2 as translate

    return translate.Client()


# Example helper to issue a simple request (wrapper)
def translate_text(client: Any, text: str, target_lang: str = "en") -> str:
    """Translate a single string.
    Args:
        client: Initialized provider client.
        text: Source text.
        target_lang: Target language code.
    Returns:
        Translated text.
    """
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]
