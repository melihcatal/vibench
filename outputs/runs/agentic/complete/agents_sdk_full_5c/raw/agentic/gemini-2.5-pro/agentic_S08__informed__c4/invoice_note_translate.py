import os
import deepl
from typing import Optional

def translate_invoice_note(text: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates invoice notes or descriptions to a target language using DeepL API.

    :param text: The text to be translated.
    :param target_lang: The target language code (e.g., 'EN-US', 'DE', 'FR').
    :return: The translated text, or None if an error occurs.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None
    except Exception as e:
        print(f"A non-DeepL error occurred: {e}")
        return None

