import os
import deepl


def translate_text(text: str, target_lang: str = "FR"):
    """
    Translates platform model output for another locale using DeepL.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French).

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang)

    return result.text
