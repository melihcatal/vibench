from translation_client import google_translate_client
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a single text string.
    """
    result = google_translate_client.translate(
        request.source_text,
        target_language=request.target_lang,
        source_language=request.source_lang,
    )
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_lang=result.get("detectedSourceLanguage", ""),
    )
