from google.cloud import translate_v3 as translate

def translate_runbook_notes(text: str, target_language_code: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
