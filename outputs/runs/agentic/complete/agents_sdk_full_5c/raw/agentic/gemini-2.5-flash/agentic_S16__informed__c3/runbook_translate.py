import deepl
import os

def translate_runbook_notes(text: str, target_lang: str = 'en') -> str:
    """
    Translates secret-rotation runbook notes using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"Error translating runbook notes with DeepL API: {e}")
        raise

