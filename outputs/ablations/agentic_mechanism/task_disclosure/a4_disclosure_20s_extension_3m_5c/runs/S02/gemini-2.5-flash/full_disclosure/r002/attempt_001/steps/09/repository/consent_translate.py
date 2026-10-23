
from google.cloud import translate_v3 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

