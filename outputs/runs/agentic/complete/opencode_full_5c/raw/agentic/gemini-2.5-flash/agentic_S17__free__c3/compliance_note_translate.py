from google.cloud import translate
from security_client import get_translate_client, PROJECT_ID
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_note(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = get_translate_client()

    parent = f"projects/{request.project_id}/locations/{request.location}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language_code,
    )

    translated_text = ""
    source_language_code = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        source_language_code = response.translations[0].detected_language_code

    return ComplianceNoteTranslateResponse(
        translated_text=translated_text, source_language_code=source_language_code
    )
