from google.cloud import translate_v3beta1 as translate

def translate_markup(
    project_id: str,
    markup_text: str,
    target_language: str,
    source_language: str = None
) -> str:
    """Translates HTML or other markup while preserving tags using Google Cloud Translation.

    Args:
        project_id: The ID of the GCP project.
        markup_text: The HTML or markup text to translate.
        target_language: The language to translate the text to (e.g., "es").
        source_language: The language of the input text (e.g., "en"). If None,
                         the API will attempt to detect the source language.

    Returns:
        The translated markup text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[markup_text],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/html",  # Specify HTML mime type
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
