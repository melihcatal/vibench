from google.cloud import translate_v3 as translate

def translate_markup(
    project_id: str,
    html_content: str,
    source_language_code: str,
    target_language_code: str,
) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        source_language_code=source_language_code,
        target_language_code=target_language_code,
        mime_type="text/html",  # Specify mime_type as HTML
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
