
import os
import deepl

def translate_invoice_note(note: str, target_lang: str = "EN-US") -> str:
    """
    Translates an invoice note or description to a target language using DeepL.

    Args:
        note: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(note, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"DeepL API error: {e}")
        return f"Translation failed: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Translation failed due to an unexpected error."
