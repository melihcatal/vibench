from google.cloud import translate_v3beta1 as translate

def translate_text(
    project_id: str,
    text: str,
    target_language: str,
    source_language: str = None
) -> str:
    """Translates a single piece of text using Google Cloud Translation.

    Args:
        project_id: The ID of the GCP project.
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es").
        source_language: The language of the input text (e.g., "en"). If None,
                         the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",  # Set mime_type to "text/html" for HTML input
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
