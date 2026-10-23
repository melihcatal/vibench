import os
from translation_client import get_translation_client, get_location_path

def translate_markup_text(
    markup_text: str,
    target_language_code: str,
    source_language_code: str = "",
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
) -> str:
    """Translates HTML/markup text using Google Cloud Translation API, preserving tags."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    client = get_translation_client()
    location_path = get_location_path(project_id)

    response = client.translate_text(
        request={
            "parent": location_path,
            "contents": [markup_text],
            "mime_type": "text/html",  # Specify HTML mime type
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
