import os
import deepl

def translate_text(text: str, target_lang: str = "DE") -> str:
    """
    Translates text to another locale using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "DE" for German).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # Provider-specific client class from the deepl SDK
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    
    return result.text
