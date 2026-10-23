import os
from google.cloud import translate_v2 as translate

# Helper client utilities
from translation_client import get_translation_client
from translation_models import validate_language_code

def batch_translate(texts: list[str], target_lang: str) -> list[str]:
    """Translates a list of strings while preserving order.

    Args:
        texts: List of source strings to translate.
        target_lang: Target language code (e.g., "es", "fr").

    Returns:
        List of translated strings in the same order as input.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    # google-cloud-translate supports batch translation via list input
    results = client.translate(texts, target_language=target_lang)
    # results is a list of dicts when input is a list of strings
    return [r['translatedText'] for r in results]

if __name__ == "__main__":
    sample = ["Hello", "World", "How are you?"]
    target = "fr"
    print([f"{t} -> {b}" for t, b in zip(sample, batch_translate(sample, target))])