import os
import deepl

def translate_script(text: str, target_lang: str = "DE") -> str:
    """
    Translates a script to the target language using the DeepL API.

    Requires the DEEPL_AUTH_KEY environment variable to be set.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "DE" for German).

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
