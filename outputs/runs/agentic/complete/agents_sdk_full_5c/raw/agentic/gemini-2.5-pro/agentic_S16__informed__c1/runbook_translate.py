import os
import deepl

def translate_runbook_notes(text: str, target_language_code: str = "DE") -> str:
    """
    Translates secret-rotation runbook notes into a specified language using DeepL.

    Args:
        text: The runbook notes in the source language (auto-detected).
        target_language_code: The target language code (e.g., "DE" for German).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # The deepl.Translator class is specific to the DeepL SDK
    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        raise
