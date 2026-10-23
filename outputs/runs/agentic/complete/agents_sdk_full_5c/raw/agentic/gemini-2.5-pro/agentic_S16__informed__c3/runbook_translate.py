import os
import deepl
from typing import Optional

def translate_runbook_text(text: str, target_language: str) -> Optional[str]:
    """
    Translates a given text into the target language using the DeepL API.

    Args:
        text (str): The text to be translated.
        target_language (str): The target language code (e.g., "DE", "FR", "ES").

    Returns:
        Optional[str]: The translated text, or None if an error occurs.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        
        # For language codes, DeepL expects uppercase (e.g., 'EN-US', 'DE')
        # This handles cases where user might input 'de' or 'fr'
        target_lang_upper = target_language.upper()

        result = translator.translate_text(text, target_lang=target_lang_upper)
        
        return result.text

    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
