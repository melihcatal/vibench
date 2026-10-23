from translation_client import get_translation_client
from translation_models import get_project_id, get_location


def translate_single_text(
    text: str, target_language: str, source_language: str = ""
) -> str:
    """Translates a single text string using Google Cloud Translation V3.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the text. If not specified, auto-detected.

    Returns:
        The translated text.
    """
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    # The response contains a list of translations. We expect one for a single text.
    if response.translations:
        return response.translations[0].translated_text
    return ""
