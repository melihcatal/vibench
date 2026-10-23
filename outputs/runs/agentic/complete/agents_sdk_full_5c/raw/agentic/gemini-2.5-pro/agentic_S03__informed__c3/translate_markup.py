from translation_client import get_translation_client, get_gcp_project_id

def translate_html(
    html_content: str, target_language: str, source_language: str
) -> str:
    """
    Translates HTML content while preserving markup.

    Args:
        html_content: An HTML string to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated HTML string.
    """
    client = get_translation_client()
    project_id = get_gcp_project_id()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/html",
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
