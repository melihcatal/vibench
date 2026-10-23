import os
import deepl

def translate_query(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates a query to a target language using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
