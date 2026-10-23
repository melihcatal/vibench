# alt_text_translate.py
# [LATER-STEP]

from __future__ import annotations

import os
from typing import Optional

# Placeholder import for translation SDK (e.g., Google Translate)
# from google.cloud import translate_v2 as translate

# Assume `os.getenv('TRANSLATION_PROJECT_ID')` returns the project ID
# translator_client = translate.Client()


def translate_text(text: str, target_lang: str) -> str:
    """Translate a simple string to a target language using a cloud translation API.

    For demonstration, this stub returns the original text. Replace the body
    with real translation SDK calls when integrating a provider.
    """
    # Example real call (uncomment and configure):
    # result = translator_client.translate(text, target_language=target_lang)
    # return result['translatedText']
    return text  # placeholder


def translate_alt_text(image_desc: str, target_lang: str = "es") -> str:
    """Generate and translate an alt text description for an image.

    Steps:
    1. Pass `image_desc` through a cloud translation API.
    2. Return the translated description.
    """
    # Placeholder: simply return the original description
    translated = translate_text(image_desc, target_lang)
    return translated
