import os
import deepl
from . import storage_models

def translate_text(
    text: str, 
    target_lang: str = "EN-US"
) -> storage_models.TranslationResult:
    """
    Translates text using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., 'EN-US', 'ES', 'FR').

    Returns:
        A TranslationResult object.
    """
    deepl_api_key = os.environ.get("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    translator = deepl.Translator(deepl_api_key)

    result = translator.translate_text(text, target_lang=target_lang)

    return storage_models.TranslationResult(
        source_text=text,
        translated_text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_lang,
    )
