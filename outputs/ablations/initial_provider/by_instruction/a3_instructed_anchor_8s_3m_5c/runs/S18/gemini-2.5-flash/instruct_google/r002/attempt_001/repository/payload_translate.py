import os
from google.cloud import translate_v3 as translate

def payload_translate(text: str, target_language_code: str) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation API.

    Args:
        text: The text content to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"  # Or a specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
