from security_client import get_translate_client
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    translate_client = get_translate_client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
