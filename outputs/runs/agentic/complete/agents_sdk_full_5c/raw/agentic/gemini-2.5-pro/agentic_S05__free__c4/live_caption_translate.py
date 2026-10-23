import os
import deepl

def translate_caption(text: str, target_lang: str = "DE"):
    """
    Translates a live caption text to a target language using DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "DE" for German).

    Returns:
        The translated text.
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
