import os
from google.cloud import translate_v2 as translate

TRANSLATE = translate.Client()

def batch_translate(texts: list[str], target_lang: str = "es") -> list[str]:
    """Translate a list of strings while preserving order using Google Cloud Translation API.
    Args:
        texts: List of source texts.
        target_lang: Target language code (ISO-639-1).
    Returns:
        List of translated texts in the same order as input.
    """
    results = TRANSLATE.translate(texts, target_language=target_lang)
    # results is a list of dicts when multiple texts are provided
    return [r['translatedText'] for r in results]