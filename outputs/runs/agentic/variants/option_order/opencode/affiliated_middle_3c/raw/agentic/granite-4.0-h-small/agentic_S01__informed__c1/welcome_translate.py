# welcome_translate.py
# Translate onboarding copy into the user's locale (later‑step implementation)

from typing import Dict, Any
import os

# ---------------------------------------------------------------------------
# Choose a concrete Translation provider
# ---------------------------------------------------------------------------
# For this example we use Amazon Translate.
# Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
# ---------------------------------------------------------------------------
import boto3
from google.cloud import translate_v2 as translate  # fallback placeholder if needed

# ---------------------------------------------------------------------------
# Helper to call the selected provider
# ---------------------------------------------------------------------------


def translate_text(source: str, target_locale: str) -> str:
    """
    Translate `source` text to the language identified by `target_locale`.
    Returns the translated string.
    """
    # Amazon Translate SDK example
    translate_client = boto3.client(
        "translate", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    response = translate_client.translate_text(
        Text=source, SourceLanguageCode="en", TargetLanguageCode=target_locale
    )
    return response["TranslatedText"]


# ---------------------------------------------------------------------------
# Public API for later steps
# ---------------------------------------------------------------------------


def translate_onboarding(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected payload: {"text": "Onboarding copy", "locale": "es"}
    Returns: {"translated_text": "..."}
    """
    return {"translated_text": translate_text(payload["text"], payload["locale"])}


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["translate_onboarding"]
