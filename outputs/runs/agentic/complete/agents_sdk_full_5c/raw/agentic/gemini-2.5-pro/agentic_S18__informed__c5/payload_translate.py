import os
import deepl

def translate_text(text: str, target_language: str = "FR") -> str:
    """
    Translates text to the target language using the DeepL API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., "FR" for French).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return f"Error: {e}"

