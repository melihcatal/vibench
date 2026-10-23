import os
import json
import base64
from typing import Dict, Any

# Use Google Cloud Translation service via google-cloud-translate SDK
from google.cloud import translate_v2 as translate

# Authenticate via env var GOOGLE_APPLICATION_CREDENTIALS (set in environment)
translator = translate.Client()

TARGET_LANG = os.getenv("COMPLIANCE_TRANSLATION_TARGET", "es")  # default Spanish


def translate_compliance_note(note: str) -> str:
    """Translate an encryption/compliance note for reviewer consumption.

    Returns the translated text.
    """
    result = translator.translate(note, target_language=TARGET_LANG)
    return result["translatedText"]
