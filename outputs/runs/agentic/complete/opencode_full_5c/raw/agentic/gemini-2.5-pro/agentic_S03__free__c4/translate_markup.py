from translation_client import get_translation_client


def translate_html(
    html_content: str, target_language: str, source_language: str = None
):
    """
    Translates HTML content while preserving markup.

    Args:
        html_content: The HTML content string to translate.
        target_language: The language to translate the content into.
        source_language: The source language of the content. If None, the API
                         will attempt to detect the source language.

    Returns:
        A dictionary containing the translated HTML content.
    """
    client = get_translation_client()
    result = client.translate(
        html_content,
        target_language=target_language,
        source_language=source_language if source_language else "",
        mime_type="text/html",
    )
    return result
