import os
from google.cloud import translate_v2 as translate
from typing import Dict


def translate_image_description(description: str, target_lang: str = "es") -> str:
    """Translate the visual description (alt text) into a target language.

    Uses Google Cloud Translation service.
    """
    client = translate.Client()
    translated = client.translate(description, target_language=target_lang)
    # The API returns the translated text under the 'translatedText' key
    return translated["translatedText"] if translated else description
