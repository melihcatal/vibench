import os
from deepl import Translator


def translate_log_message(text: str, target_lang: str = "ES") -> str:
    """
    Translates support-visible log messages to another locale using DeepL API.

    Args:
        text: The log message text to translate.
        target_lang: Target language code (e.g., "ES", "DE", "FR").

    Returns:
        Translated log message text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = Translator(auth_key=auth_key)

    result = translator.translate_text(text, target_lang=target_lang)

    return result.text
