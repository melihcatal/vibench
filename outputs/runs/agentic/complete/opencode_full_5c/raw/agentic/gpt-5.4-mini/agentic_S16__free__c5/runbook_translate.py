from google.cloud import translate_v3


def runbook_translate(text: str, project_id: str, target_language_code: str = "es"):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text
