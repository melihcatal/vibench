import os
import deepl
from typing import Optional

def translate_appeal_text(text: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates text for an appeal using the DeepL API.
    
    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").
    
    Returns:
        The translated text, or None if translation fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        return None
    except Exception as e:
        print(f"A non-DeepL error occurred: {e}")
        return None
