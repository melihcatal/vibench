from translation_client import (
    get_source_language,
    get_target_language,
    get_translation_client,
)
from translation_models import TranslationResponse, normalize_text


def translate_markup(
    markup: str, source_language: str, target_language: str
) -> TranslationResponse:
    client = get_translation_client()
    result = client.translate_text(
        normalize_text(markup),
        source_lang=get_source_language(source_language),
        target_lang=get_target_language(target_language),
        tag_handling="html",
    )
    return TranslationResponse(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        provider="deepl",
    )
