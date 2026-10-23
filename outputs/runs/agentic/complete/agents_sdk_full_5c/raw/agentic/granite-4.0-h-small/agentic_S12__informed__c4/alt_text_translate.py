import os
from typing import List, Dict

import requests
from google.cloud.translate_v2 import Client as TranslationClient

# -------------------------------------------------------------------
# Translate generated image captions / descriptions into other languages
# -------------------------------------------------------------------

def translate_caption(caption: str, target_lang: str = 'es') -> str:
    """Translate a single caption using Google Cloud Translation.

    Returns the translated string.  Raises for unrecoverable errors.
    """
    # Explicit client creation; credentials loaded from GOOGLE_APPLICATION_CREDENTIALS
    translator = TranslationClient()
    result = translator.translate(caption, target_language=target_lang)
    return result['translatedText']


def bulk_translate(captions: List[str], target_lang: str = 'fr') -> List[str]:
    """Translate a list of captions in batch (single API call where possible)."""
    translator = TranslationClient()
    # TranslationClient.translate_batch accepts a list of texts
    results = translator.translate(captions, target_language=target_lang)
    # Each entry contains 'translatedText'
    return [res['translatedText'] for res in results]


def translate_from_file(input_path: str, output_path: str, target_lang: str = 'de') -> None:
    """Read a JSON file containing captions, translate, and write the translated list back.",
    with open(input_path, 'r', encoding='utf-8') as f:
        captions = json.load(f)
    translated = bulk_translate(captions, target_lang)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
