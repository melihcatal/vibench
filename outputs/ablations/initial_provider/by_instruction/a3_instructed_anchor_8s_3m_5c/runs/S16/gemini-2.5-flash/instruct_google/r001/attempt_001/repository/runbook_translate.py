from google.cloud import translate_v3 as translate

def translate_runbook_notes(project_id: str, text: str, target_language_code: str = "en") -> str:
    client = translate.TranslationServiceClient()
    location = "global" # For Translation API, 'global' is often used for non-regionalized endpoints
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
    return translated_text
