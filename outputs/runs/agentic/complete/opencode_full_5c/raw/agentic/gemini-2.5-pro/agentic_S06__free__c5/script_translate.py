import os
import deepl


def script_translate(text: str, target_lang: str = "FR"):
    """
    Translates a script to the target language using DeepL.

    Args:
        text (str): The text to translate.
        target_lang (str): The target language code (e.g., "FR" for French).

    Returns:
        str: The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
