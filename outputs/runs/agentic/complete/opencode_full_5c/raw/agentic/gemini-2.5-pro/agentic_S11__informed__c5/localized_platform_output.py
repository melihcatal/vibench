import os
import deepl

from model_models import TranslationResponse


def translate_text(
    text_to_translate: str, target_language: str = "FR"
) -> TranslationResponse:
    """
    Translates platform model output for another locale using DeepL.

    Args:
        text_to_translate: The text to be translated.
        target_language: The target language code (e.g., "FR" for French).

    Returns:
        A TranslationResponse object containing the translated text.
    """
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text_to_translate, target_lang=target_language)

    return TranslationResponse(
        translated_text=result.text,
        detected_source_language=result.detected_source_lang,
    )
