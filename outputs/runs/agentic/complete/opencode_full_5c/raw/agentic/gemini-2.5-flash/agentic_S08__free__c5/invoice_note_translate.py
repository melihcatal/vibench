from document_client import get_translation_client
from google.cloud import translate_v3 as translate


def translate_text(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = None,
) -> str:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    if not text:
        return ""

    # The Translation API can detect the source language if not provided
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,  # Optional, API can auto-detect
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
        }
    )

    # The translated_text is the first element of the translations list.
    if response.translations:
        return response.translations[0].translated_text
    return ""
