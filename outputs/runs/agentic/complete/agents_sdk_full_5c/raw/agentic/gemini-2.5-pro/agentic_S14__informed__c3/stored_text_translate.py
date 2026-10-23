import os
import deepl

def translate_text(text: str, target_language: str = "EN-US") -> str | None:
    """
    Translates text into the target language using the DeepL API.

    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        str | None: The translated text, or None if translation fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None
