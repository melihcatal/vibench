from translation_client import get_translation_client


def translate_markup(
    html_content: str, target_language_code: str, source_language_code: str = "en"
) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = get_translation_client()
    project_id = ""  # Replace with your Google Cloud Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [html_content],
            "mime_type": "text/html",  # Specify the mime type as HTML
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
