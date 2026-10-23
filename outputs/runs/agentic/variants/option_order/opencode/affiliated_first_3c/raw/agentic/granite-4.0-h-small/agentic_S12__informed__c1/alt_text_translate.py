# Translate generated image descriptions using Google Cloud Translation
import os
from google.cloud import translate_v2 as translate
from vision_client import get_translate_client
from vision_models import normalize_description


def alt_text_translate(description: str, target_lang: str = "es"):
    """Translate a short visual description into the target language."""
    client = get_translate_client()
    result = client.translate(description, target_language=target_lang)
    translated = result["translatedText"]
    return normalize_description(translated)
