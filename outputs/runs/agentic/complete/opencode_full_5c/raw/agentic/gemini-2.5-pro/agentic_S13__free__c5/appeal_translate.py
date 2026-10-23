from safety_client import get_deepl_translator
from safety_models import TranslationResponse


def translate_appeal_text(
    text: str, target_language: str = "EN-US"
) -> TranslationResponse:
    """
    Translate appeal text for review using the DeepL API.
    """
    translator = get_deepl_translator()
    result = translator.translate_text(text, target_lang=target_language)

    return TranslationResponse(
        translated_text=result.text,
        detected_source_language=result.detected_source_lang,
    )
