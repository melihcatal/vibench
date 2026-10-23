from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language_code: str, target_language_code: str) -> TranslationResponse:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language_code=normalize_text(source_language_code),
        target_language_code=normalize_text(target_language_code),
    )
    client = get_translation_client()
    translated_text = client.translate_text(request.text, request.source_language_code, request.target_language_code)
    return TranslationResponse(
        translated_text=translated_text,
        source_language_code=request.source_language_code,
        target_language_code=request.target_language_code,
        provider="aws.translate",
    )
