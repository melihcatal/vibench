from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, TranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    """
    Translates HTML or other markup, preserving tags.
    """
    client = get_translation_client()
    result = client.translate(
        request.markup,
        target_language=request.target_language,
        source_language=request.source_language,
        format_="html",
    )
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage", ""),
    )
