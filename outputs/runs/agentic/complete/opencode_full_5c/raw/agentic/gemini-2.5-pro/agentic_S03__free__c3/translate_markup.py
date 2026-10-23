from translation_client import google_translate_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    """
    Translates HTML or other markup.
    """
    result = google_translate_client.translate(
        request.source_markup,
        target_language=request.target_lang,
        source_language=request.source_lang,
        mime_type="text/html",
    )
    return MarkupTranslationResponse(
        translated_markup=result["translatedText"],
        detected_source_lang=result.get("detectedSourceLanguage", ""),
    )
