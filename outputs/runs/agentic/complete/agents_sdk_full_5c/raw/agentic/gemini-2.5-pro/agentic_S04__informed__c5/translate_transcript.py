import os
import deepl

def translate_text(text: str, target_lang: str = "FR") -> str:
    """
    Translates text using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    
    if isinstance(result, deepl.TextResult):
        return result.text
    # Handle list of results if input text is a list
    if isinstance(result, list) and result:
        return result[0].text
        
    return ""
