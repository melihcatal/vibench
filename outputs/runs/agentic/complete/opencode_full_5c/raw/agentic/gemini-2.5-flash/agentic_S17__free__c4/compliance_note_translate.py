import os
from typing import Optional
from security_client import SecurityClient
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_notes(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = SecurityClient()
    translated_text, detected_language_code = client.translate_text_with_gcp_translate(
        project_id=request.project_id,
        location_id=request.location_id,
        text=request.text,
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
    )
    return ComplianceNoteTranslateResponse(
        translated_text=translated_text, detected_language_code=detected_language_code
    )
