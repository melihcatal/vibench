from security_client import SecurityClient
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_note(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    client = SecurityClient()
    response = client.translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode="auto",  # Let Amazon Translate detect the source language
        TargetLanguageCode=request.target_language,
    )
    return ComplianceNoteTranslateResponse(translated_text=response["TranslatedText"])
