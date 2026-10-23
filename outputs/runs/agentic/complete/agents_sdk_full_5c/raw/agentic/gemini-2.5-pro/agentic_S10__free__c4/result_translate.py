import os
import deepl

def translate_text(text: str, target_lang: str = "DE") -> str | None:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "DE", "FR", "ES").

    Returns:
        The translated text, or None if an error occurs.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
