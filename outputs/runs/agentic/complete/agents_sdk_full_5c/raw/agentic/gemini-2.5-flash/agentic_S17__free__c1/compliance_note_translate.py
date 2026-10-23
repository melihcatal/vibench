from google.cloud import translate_v3 as translate

def translate_compliance_note(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates an encryption or compliance note using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
