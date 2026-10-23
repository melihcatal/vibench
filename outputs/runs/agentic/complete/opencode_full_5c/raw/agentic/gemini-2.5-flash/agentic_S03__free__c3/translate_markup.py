from translation_client import get_translation_client
from translation_models import get_project_id, get_location


def translate_html_markup(
    html_content: str, target_language: str, source_language: str = ""
) -> str:
    """Translates HTML content using Google Cloud Translation V3, preserving tags.

    Args:
        html_content: The HTML string to translate.
        target_language: The language to translate the HTML to (e.g., "es" for Spanish).
        source_language: The language of the HTML. If not specified, auto-detected.

    Returns:
        The translated HTML string.
    """
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        mime_type="text/html",  # Specify mime_type as text/html
        source_language_code=source_language,
        target_language_code=target_language,
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
