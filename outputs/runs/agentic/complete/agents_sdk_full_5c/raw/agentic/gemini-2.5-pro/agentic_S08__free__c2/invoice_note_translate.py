import os
import deepl
from typing import Optional

def invoice_note_translate(text: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates invoice notes or descriptions using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
