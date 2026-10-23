import os
import deepl

def translate_text_with_deepl(text: str, target_language: str = "EN-US") -> str:
    """
    Translates text using the DeepL API.

    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        str: The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
