from google.cloud import translate_v3
from security_client import get_translate_client
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)
import os


def translate_compliance_notes(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = get_translate_client()
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # Or other method to get project_id
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
        }
    )

    translated_text = ""
    detected_source_language = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return ComplianceNoteTranslateResponse(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=request.target_language,
    )
