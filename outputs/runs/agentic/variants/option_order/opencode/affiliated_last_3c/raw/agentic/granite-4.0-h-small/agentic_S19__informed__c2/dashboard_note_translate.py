# [LATER-STEP] dashboard_note_translate.py

# Translate metric or dashboard notes for another locale using Google Cloud Translation.
# Provider: Cloud Translation (google-cloud-translate SDK)

import os
from typing import Dict

from google.cloud import translate_v2 as translate


def translate_note(note_text: str, target_lang: str = "es") -> Dict[str, str]:
    """
    Translates *note_text* into the target language using Google Cloud Translation.
    The function authenticates using GOOGLE_APPLICATION_CREDENTIALS env var.

    Returns a dict with the original text and the translated text.
    """
    client = translate.Client()
    result = client.translate(note_text, target_language=target_lang)
    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "detected_source_language": result.get("src", "en"),
    }
