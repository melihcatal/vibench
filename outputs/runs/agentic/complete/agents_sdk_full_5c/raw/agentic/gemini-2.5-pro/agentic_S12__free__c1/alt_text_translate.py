import os
import deepl

from vision_models import ImageDescription

def translate_description(description: ImageDescription, target_language: str = "DE") -> str:
    """
    Translates an image description to a target language using the DeepL API.

    Args:
        description: The ImageDescription object containing the text to translate.
        target_language: The target language code (e.g., "DE" for German, "FR" for French).

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(description.text, target_lang=target_language)
    
    return result.text
