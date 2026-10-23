import os
import json
from safety_client import get_client

# LATER-STEP
# Translate an appeal text into a review-friendly format using an external translation service.
# Provider identification: GOOGLE (Google Cloud Translation)


def translate_appeal(text: str, target_lang: str = "en") -> str:
    """Translate appeal text to improve reviewer understanding.

    Uses Google Cloud Translation API.
    """
    client = get_client("google")
    if client is None:
        raise RuntimeError("Google client not configured")
    translate = client.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_lang,
            "model": os.getenv("GOOGLE_TRANSLATION_MODEL", "nmt"),
        }
    )
    translated = response.translations[0].translated_text
    return translated
