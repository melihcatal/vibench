import os
from google.cloud import translate_v3beta1 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation API.

    Args:
        text: The appeal text to translate.
        target_language: The language to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="auto",  # Automatically detect source language
        target_language_code=target_language,
    )

    if response.translations:
        return response.translations[0].translated_text
    return text

