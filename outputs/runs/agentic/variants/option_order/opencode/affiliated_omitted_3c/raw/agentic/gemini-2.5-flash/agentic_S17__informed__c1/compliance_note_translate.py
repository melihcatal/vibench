import json

from security_client import get_translate_client
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_notes(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        return ComplianceNoteTranslateResponse(
            translated_text=response["TranslatedText"],
            source_language_code=response["SourceLanguageCode"]
            if "SourceLanguageCode" in response
            else request.source_language_code,
            target_language_code=response["TargetLanguageCode"]
            if "TargetLanguageCode" in response
            else request.target_language_code,
        )
    except Exception as e:
        raise RuntimeError(
            f"Error translating compliance notes with Amazon Translate: {e}"
        )
