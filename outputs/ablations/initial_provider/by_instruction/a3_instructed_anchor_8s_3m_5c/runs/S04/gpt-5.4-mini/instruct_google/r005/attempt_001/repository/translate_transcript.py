from google.cloud import translate_v3 as translate


def translate_transcript(text: str, target_language: str, project_id: str, location: str = "global"):
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
