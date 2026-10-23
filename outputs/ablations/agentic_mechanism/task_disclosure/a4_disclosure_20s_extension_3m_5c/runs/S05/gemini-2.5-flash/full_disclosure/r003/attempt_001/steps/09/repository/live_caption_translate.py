import os
from google.cloud import translate

def translate_caption_chunk(text_content: str, target_language: str) -> str:
    """Translates a chunk of text using Google Cloud Translation.

    Args:
        text_content: The text chunk to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    # The project ID and location can be set as environment variables or explicitly.
    # For this example, we'll assume GOOGLE_CLOUD_PROJECT is set.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
