import os
from google.cloud import translate

# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment


def translate_consent_copy(text: str, target_language: str, project_id: str) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The consent copy text to translate.
        target_language: The target language code (e.g., "es", "fr").
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.

    Raises:
        Exception: If translation fails.
    """
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # or "text/html"
            "target_language_code": target_language,
        }
    )

    # Assuming only one translation is requested
    if response.translations:
        return response.translations[0].translated_text
    else:
        raise Exception("No translation received.")
