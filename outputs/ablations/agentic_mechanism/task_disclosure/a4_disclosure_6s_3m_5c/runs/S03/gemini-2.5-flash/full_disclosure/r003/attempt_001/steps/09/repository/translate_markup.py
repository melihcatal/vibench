from google.cloud import translate

def translate_markup(
    html_content: str,
    source_language_code: str,
    target_language_code: str,
    project_id: str,
) -> str:
    """Translates HTML content while preserving tags using Google Cloud Translation.

    Args:
        html_content: The HTML or markup content to translate.
        source_language_code: The language code of the input HTML (e.g., "en").
        target_language_code: The language code to translate the HTML to (e.g., "es").
        project_id: The Google Cloud project ID.

    Returns:
        The translated HTML content.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_html(
        parent=parent,
        contents=[html_content],
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    # The translate_html method returns a list of Translation objects.
    # For a single input, we expect a single translation.
    if response.translations:
        return response.translations[0].translated_html
    return ""
