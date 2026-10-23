import deepl
import os
from translation_client import get_deepl_client

def translate_single_text(text: str, target_lang: str, source_lang: str = None) -> str:
    """
    Translates a single text string using DeepL.
    """
    client = get_deepl_client()
    result = client.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang
    )
    return result.text

if __name__ == '__main__':
    # Example usage (ensure DEEPL_AUTH_KEY is set in environment variables)
    text_to_translate = "Hello, world!"
    target_language = "fr"
    translated_text = translate_single_text(text_to_translate, target_language)
    print(f"Original: {text_to_translate}")
    print(f"Translated ({target_language}): {translated_text}")
