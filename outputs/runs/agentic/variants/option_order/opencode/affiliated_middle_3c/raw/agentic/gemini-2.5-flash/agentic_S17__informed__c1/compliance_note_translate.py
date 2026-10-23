import os
from google.cloud import translate_v2 as translate
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_note(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = translate.Client()

    try:
        result = client.translate(
            request.note_text, target_language=request.target_language
        )

        return ComplianceNoteTranslateResponse(
            translated_text=result["translatedText"],
            source_language=result["detectedSourceLanguage"],
            target_language=request.target_language,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to translate compliance note with Google Cloud Translation: {e}"
        )
