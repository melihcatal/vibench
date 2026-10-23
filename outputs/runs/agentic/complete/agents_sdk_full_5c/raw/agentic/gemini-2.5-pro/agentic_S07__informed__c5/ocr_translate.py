import os
import deepl

def translate_text(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates text using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    
    if isinstance(result, deepl.TextResult):
        return result.text
    # Handle list of results if input was a list, though we send a string
    elif isinstance(result, list) and result:
        return result[0].text
    return ""
