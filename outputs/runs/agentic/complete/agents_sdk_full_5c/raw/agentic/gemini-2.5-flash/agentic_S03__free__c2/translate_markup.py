import os
from google.cloud import translate_v3

def translate_markup(
    project_id: str,
    html_content: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [html_content],
            "mime_type": "text/html",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""

