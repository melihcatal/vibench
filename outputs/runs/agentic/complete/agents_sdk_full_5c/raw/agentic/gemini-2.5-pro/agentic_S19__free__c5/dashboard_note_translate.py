
import os
import deepl

def translate_note(text: str, target_language: str = "DE") -> str:
    """
    Translates a metric or dashboard note into another language using DeepL.

    Args:
        text: The text content to translate.
        target_language: The target language code (e.g., "DE", "FR", "ES").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"

