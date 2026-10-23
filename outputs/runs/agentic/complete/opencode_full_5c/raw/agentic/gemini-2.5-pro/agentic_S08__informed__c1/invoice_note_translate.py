import os
import deepl
from typing import Optional


def invoice_note_translate(note: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates an invoice note to the target language using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(note, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation: {e}")
        return None
