# [LATER-STEP] compliance_note_translate.py
import json
from google.cloud import translate_v2 as translate

# Translate encryption or compliance notes for reviewers


def translate_note(note: str, target_lang: str = "es") -> dict:
    """Translates an English compliance/encryption note into the target language.

    Uses Google Cloud Translation API.
    Returns the translated text and the detected source language.
    """
    client = translate.Client()
    result = client.translate(note, target_language=target_lang)
    return {
        "original": note,
        "detected_source_language": result["src"],
        "target_language": target_lang,
        "translated_text": result["translatedText"],
        "provider": "google-cloud-translation",
    }
