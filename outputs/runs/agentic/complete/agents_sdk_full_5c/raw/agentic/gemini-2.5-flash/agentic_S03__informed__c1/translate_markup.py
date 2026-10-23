from google.cloud import translate_v3 as translate

def translate_html_markup(html_content: str, target_language: str, project_id: str, source_language: str = None) -> str:
    """Translates HTML or markup while preserving tags.

    Args:
        html_content: The HTML content to translate.
        target_language: The language to translate to.
        project_id: Your Google Cloud project ID.
        source_language: The language of the HTML. If not specified, auto-detected.

    Returns:
        The translated HTML content.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/html", # Specify HTML mime type
    )

    return response.translations[0].translated_text
