import os
import deepl
from vision_models import ImageDescription

def translate_description(
    description: ImageDescription, target_lang: str = "DE"
) -> str:
    """
    Translates an image description to a target language using DeepL.

    Args:
        description: An ImageDescription object.
        target_lang: The target language code (e.g., "DE" for German).

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(description.text, target_lang=target_lang)
    return result.text
