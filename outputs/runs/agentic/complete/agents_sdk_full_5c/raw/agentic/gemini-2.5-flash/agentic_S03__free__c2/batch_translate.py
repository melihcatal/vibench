import os
from google.cloud import translate_v3

def batch_translate_texts(
    project_id: str,
    texts: list[str],
    target_language: str,
    source_language: str = "en",
) -> list[str]:
    """Translates a list of text strings while preserving order using Google Cloud Translation."""
    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    return [translation.translated_text for translation in response.translations]

