from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(
    request: TranslationRequest,
) -> TranslationResponse:
    """Translates text containing HTML or other markup."""
    client = get_translation_client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_="html"
    )
    
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
