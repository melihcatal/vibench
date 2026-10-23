# alt_text_translate.py
import json
import uuid
from google.cloud import translate_v2 as translate
from vision_models import normalize_text

def translate_alt_text(alt_text: str, target_language: str = "es") -> str:
    """Translate image description/caption into target language using Google Cloud Translation."""
    client = translate.Client()
    # Translation auto-detects source language
    result = client.translate(alt_text, target_language=target_language)
    translated = result[\"translatedText\"]
    return normalize_text(translated)
