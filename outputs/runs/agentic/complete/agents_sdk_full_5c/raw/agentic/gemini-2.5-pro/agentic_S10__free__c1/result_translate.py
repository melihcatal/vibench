import os
import deepl
from model_client import DEEPL_API_KEY

def translate_text(text: str, target_language: str = "FR") -> str:
    """
    Translates text to a target language using the DeepL API.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "FR" for French).

    Returns:
        The translated text.
    """
    if not DEEPL_API_KEY:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred with DeepL: {e}"
