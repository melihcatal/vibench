from google.cloud import translate_v3
from security_client import SecurityClients
from security_models import ComplianceNoteTranslateRequest, ComplianceNoteTranslateResponse

def translate_compliance_note(request: ComplianceNoteTranslateRequest) -> ComplianceNoteTranslateResponse:
    translate_client = SecurityClients.get_translate_client()

    parent = f"projects/{request.project_id}/locations/global"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text_content],
            "target_language_code": request.target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return ComplianceNoteTranslateResponse(translated_text=translated_text)
