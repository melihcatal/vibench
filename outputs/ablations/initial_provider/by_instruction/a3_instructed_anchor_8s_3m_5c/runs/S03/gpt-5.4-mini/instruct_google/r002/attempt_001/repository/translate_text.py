from translation_client import get_default_source_language, get_default_target_language, get_translation_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language: str = None, target_language: str = None) -> TranslationResponse:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_text(source_language) or get_default_source_language(),
        target_language=normalize_text(target_language) or get_default_target_language(),
    )
    client = get_translation_client()
    result = client.translate(request.text, source_language=request.source_language, target_language=request.target_language)
    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=request.source_language,
        target_language=request.target_language,
        provider="google-cloud-translate-v2",
    )
