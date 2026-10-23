import os
import deepl
from model_models import TranslationResult


def translate_text(
    text_to_translate: str, target_language_code: str
) -> TranslationResult:
    """
    Translates text to a target language using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text_to_translate, target_lang=target_language_code
    )

    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_lang,
        raw_result=result,
    )
