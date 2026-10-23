from google.cloud import translate_v3 as translate
import os


def translate_text(text: str, target_language_code: str) -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.
    Provider: Google Cloud Translation
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="en",  # Assuming English as source language for alt text
        target_language_code=target_language_code,
    )

    if response.translations:
        return response.translations[0].translated_text
    return "Translation failed."
