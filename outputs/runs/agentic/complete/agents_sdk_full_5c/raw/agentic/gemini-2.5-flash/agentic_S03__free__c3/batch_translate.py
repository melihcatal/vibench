import os
from typing import List
from translation_client import get_translation_client, get_location_path

def batch_translate_texts(
    texts: List[str],
    target_language_code: str,
    source_language_code: str = "",
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
) -> List[str]:
    """Translates a list of strings using Google Cloud Translation API."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    client = get_translation_client()
    location_path = get_location_path(project_id)

    response = client.translate_text(
        request={
            "parent": location_path,
            "contents": texts,
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    return [translation.translated_text for translation in response.translations]
