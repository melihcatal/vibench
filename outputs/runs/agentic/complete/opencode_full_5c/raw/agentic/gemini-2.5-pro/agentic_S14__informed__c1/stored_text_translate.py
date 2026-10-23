import os
import deepl
from storage_models import TranslationResult


def translate_text(text: str, target_language: str = "EN-US") -> TranslationResult:
    """
    Translates text using the DeepL API.
    Requires DEEPL_AUTH_KEY to be set in the environment.

    :param text: The text to translate.
    :param target_language: The target language code (e.g., "EN-US", "DE", "FR").
    :return: A TranslationResult object.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)

    return TranslationResult(
        translated_text=result.text, source_language=result.detected_source_lang
    )
