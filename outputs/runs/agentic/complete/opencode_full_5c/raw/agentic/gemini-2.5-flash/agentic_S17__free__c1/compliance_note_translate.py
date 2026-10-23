import os
from google.cloud import translate_v3
from security_client import get_translation_client
from security_models import ComplianceNoteTranslateRequest


def translate_compliance_note(request: ComplianceNoteTranslateRequest) -> str:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/global"

    # Google Cloud Translation signal: google.cloud.translate_v3.TranslationServiceClient
    # Google Cloud Translation signal: client.translate_text
    response = client.translate_text(
        request=translate_v3.TranslateTextRequest(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language_code,
        )
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
