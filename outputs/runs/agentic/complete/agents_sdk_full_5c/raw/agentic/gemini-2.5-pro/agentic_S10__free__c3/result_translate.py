import os
import deepl

def translate_text(text: str, target_lang: str = "FR") -> str:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_API_KEY")
    if not auth_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    # Provider-specific client class: deepl.Translator
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    
    return result.text
