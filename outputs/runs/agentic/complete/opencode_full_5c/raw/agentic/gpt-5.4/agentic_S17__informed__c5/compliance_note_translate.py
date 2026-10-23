from __future__ import annotations

from security_client import DEEPL_PROVIDER, get_deepl_client
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def compliance_note_translate(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = get_deepl_client()
    result = client.translate_text(
        request.text,
        target_lang=request.target_language,
        source_lang=request.source_language,
    )
    return ComplianceNoteTranslateResponse(
        provider=DEEPL_PROVIDER,
        translated_text=result.text,
        target_language=request.target_language,
        detected_source_language=result.detected_source_lang,
    )
