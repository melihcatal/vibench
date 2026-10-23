from speech_client import get_translation_client
from speech_models import TranslationRequest, TranslationResponse


def script_translate(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()

    result = client.translate(
        request.text,
        target_language=request.target_language_code,
        source_language=request.source_language_code,
    )

    return TranslationResponse(translated_text=result["translatedText"])
