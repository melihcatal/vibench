from translation_client import get_translation_client

def translate_html(
    html_content: str, target_language_code: str, source_language_code: str = "en-US"
) -> str:
    """
    Translates HTML content while preserving markup.

    Args:
        html_content: An HTML string.
        target_language_code: The ISO 639-1 language code of the target language.
        source_language_code: The ISO 639-1 language code of the source language.

    Returns:
        The translated HTML string.
    """
    client, parent = get_translation_client()

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/html",
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
