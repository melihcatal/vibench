
"""
compliance_note_translate.py - Translate encryption or compliance notes for reviewers using Google Cloud Translation API.
"""

from google.cloud import translate_v3 # Provider-identifying signal
from security_models import ComplianceNoteTranslateRequest, ComplianceNoteTranslateResponse

def translate_compliance_note(request: ComplianceNoteTranslateRequest) -> ComplianceNoteTranslateResponse:
    translate_client = translate_v3.TranslationServiceClient()

    # The Translation API hostname is translation.googleapis.com, implicitly used by the client.
    parent = f"projects/{request.project_id}/locations/global" # Translation API often uses 'global' location

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
        }
    )

    translated_text = ""
    detected_language_code = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        # Detected language is available if not explicitly provided in the request or if auto-detected
        if response.translations[0].detected_language_code:
            detected_language_code = response.translations[0].detected_language_code

    return ComplianceNoteTranslateResponse(
        translated_text=translated_text,
        detected_language_code=detected_language_code
    )
