from google.cloud import translate_v2 as translate
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_note(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    """
    Translate encryption or compliance notes for reviewers using Google Cloud Translation.
    GOOGLE_APPLICATION_CREDENTIALS must be set in the environment.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        request.note,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return ComplianceNoteTranslateResponse(
        translated_note=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
