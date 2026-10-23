import os
import deepl
from storage_models import TranslationResult

def translate_text(
    text: str, target_lang: str, source_lang: str = None
) -> TranslationResult:
    """
    Translates text using the DeepL API.

    Requires the DEEPL_AUTH_KEY environment variable to be set.

    :param text: The text to translate.
    :param target_lang: The target language code (e.g., "EN-US", "DE", "FR").
    :param source_lang: Optional source language code.
    :return: A TranslationResult object.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(
            text, source_lang=source_lang, target_lang=target_lang
        )

        return TranslationResult(
            original_text=text,
            translated_text=result.text,
            source_language=result.detected_source_lang,
            target_language=target_lang,
        )
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        raise
