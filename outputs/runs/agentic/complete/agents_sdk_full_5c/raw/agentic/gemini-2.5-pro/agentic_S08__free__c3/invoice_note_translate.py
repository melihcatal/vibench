import os
import deepl
from typing import Optional

def translate_text(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> Optional[str]:
    """
    Translates a given text into the target language using the DeepL API.
    
    :param text: The text to be translated.
    :param target_lang: The target language code (e.g., "EN-US", "DE", "FR").
    :param source_lang: The source language code. If None, DeepL auto-detects.
    :return: The translated text, or None if an error occurs.
    """
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(api_key)
        result = translator.translate_text(
            text,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
