import os
from translation_client import get_google_translate_client

def translate_single_text(
    text: str,
    source_language_code: str,
    target_language_code: str,
    project_id: str
) -> str:
    client = get_google_translate_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
