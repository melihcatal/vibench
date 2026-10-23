import os
import deepl

def translate_runbook_notes(text: str, target_language: str = "JA") -> str | None:
    """
    Translates runbook notes for secret rotation procedures to another language.
    
    This helps international teams follow standardized procedures.

    Args:
        text: The text to be translated.
        target_language: The target language code (e.g., "DE", "FR", "JA").
                         See DeepL documentation for supported languages.

    Returns:
        The translated text as a string, or None on failure.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        print("DEEPL_AUTH_KEY environment variable not set.")
        return None

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except Exception as e:
        print(f"An error occurred during translation with DeepL: {e}")
        return None
