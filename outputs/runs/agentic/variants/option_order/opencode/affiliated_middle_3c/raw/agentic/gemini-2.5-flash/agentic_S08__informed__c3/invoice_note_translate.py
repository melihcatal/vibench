import os
from typing import Optional, List
from google.cloud import (
    translate_v2 as translate,
)  # Provider identifiable import: Google Cloud Translation

# Configure Google Cloud Translation
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
# For local development, this typically points to a service account key file.
# In Google Cloud environments, credentials are automatically handled.


def translate_invoice_note(text: str, target_language: str = "en") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    This function is a scored component.
    """
    # Client will automatically pick up GOOGLE_APPLICATION_CREDENTIALS
    translate_client = translate.Client()

    if not text.strip():
        return ""

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating invoice note with Google Cloud Translation API: {e}")
        return None
