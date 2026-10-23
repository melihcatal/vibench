import os
import deepl


def translate_log_message(
    log_message: str, target_lang: str = "en", source_lang: str = None
) -> str:
    """Translates support-visible log messages for another locale using DeepL API.

    Args:
        log_message: The log message text to translate.
        target_lang: The target language for the translation (e.g., "en", "fr", "de").
                     Defaults to "en" (English).
        source_lang: The source language of the log message. If None, DeepL will auto-detect.

    Returns:
        The translated log message.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            text=log_message,
            target_lang=target_lang.upper(),  # DeepL expects uppercase for target_lang
            source_lang=source_lang.upper() if source_lang else None,
        )
        return result.text
    except deepl.exceptions.DeepLException as e:
        return f"Error translating log message: {e}"
