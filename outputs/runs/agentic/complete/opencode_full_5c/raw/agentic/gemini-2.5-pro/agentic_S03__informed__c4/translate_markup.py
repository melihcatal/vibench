from translation_client import get_translation_client
from translation_models import TranslationResponse


def translate_markup(
    markup: str, target_language: str, source_language: str | None = None
) -> TranslationResponse:
    """
    Translates HTML or other markup, preserving tags.
    """
    client = get_translation_client()
    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language if source_language else "",
        format_="html",
    )
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
