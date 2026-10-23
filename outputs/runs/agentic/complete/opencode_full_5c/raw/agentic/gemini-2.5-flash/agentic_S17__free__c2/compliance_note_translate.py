from security_client import SecurityClient
from security_models import ComplianceNote


def translate_compliance_note(
    note: ComplianceNote, target_language_code: str, project_id: str
) -> ComplianceNote:
    client = SecurityClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [note.text],
            "mime_type": "text/plain",
            "source_language_code": note.language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return ComplianceNote(language_code=target_language_code, text=translated_text)
