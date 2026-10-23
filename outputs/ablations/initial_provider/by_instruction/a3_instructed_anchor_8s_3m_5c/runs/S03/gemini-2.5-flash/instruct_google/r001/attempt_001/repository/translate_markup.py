import os
from translation_client import get_translation_client

def translate_html_markup(
    html_content: str, target_language: str, source_language: str = ""
) -> str:
    """Translates HTML or other markup content using Google Cloud Translation API, preserving tags.

    Args:
        html_content: The HTML or markup string to translate.
        target_language: The language to translate the content to (e.g., 'es' for Spanish).
        source_language: The language of the input content (e.g., 'en' for English).
                         If not specified, Google will auto-detect.

    Returns:
        The translated HTML or markup content.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable not set. "
            "Please set it to your Google Cloud Project ID."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [html_content],
            "mime_type": "text/html",  # Specify that the content is HTML
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else None,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
