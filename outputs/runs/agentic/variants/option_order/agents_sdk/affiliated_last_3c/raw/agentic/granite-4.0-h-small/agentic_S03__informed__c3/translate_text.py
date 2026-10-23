import os
from google.cloud import translate_v2 as translate

# Helper client utilities are imported from local modules
from translation_client import get_translation_client
from translation_models import validate_language_code

def translate_text(source_text: str, target_lang: str) -> str:
    """Translates a single string between languages using Google Cloud Translation.

    Args:
        source_text: The source text to translate.
        target_lang: Target language code (e.g., "es", "fr").

    Returns:
        The translated text.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    result = client.translate(source_text, target_language=target_lang)
    return result['translatedText']

if __name__ == "__main__":
    # Example usage (remove or protect credentials in production)
    text = "Hello, world!"
    target = "es"
    print(f"Translated: {translate_text(text, target)}")