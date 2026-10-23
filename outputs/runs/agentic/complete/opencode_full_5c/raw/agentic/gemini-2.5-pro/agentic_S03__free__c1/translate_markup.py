from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
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
    return MarkupTranslationResponse(translated_markup=result["translatedText"])
