from google.cloud import translate_v3 as translate
import os


def translate_text_with_google(
    text: str, project_id: str, target_language: str = "en"
) -> str:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
