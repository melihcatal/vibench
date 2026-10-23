import os
from google.cloud import translate_v3

def translate_text(
    project_id: str,
    text: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""

