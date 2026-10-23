from google.cloud import translate

def translate_text(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.TranslationServiceClient()
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your Google Cloud Project ID
    parent = f"projects/{project_id}/locations/global"

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language,
            }
        )

    return response.translations[0].translated_text
