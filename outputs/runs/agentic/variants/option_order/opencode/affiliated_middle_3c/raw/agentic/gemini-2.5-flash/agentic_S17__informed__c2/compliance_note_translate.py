from security_client import security_client
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    result = security_client.translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    translated_text = result["translatedText"]
    detected_source_language = result.get("detectedSourceLanguage")

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
