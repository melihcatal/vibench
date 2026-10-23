import os
from google.cloud import translate_v3 as translate

def translate_onboarding_copy(text: str, target_language_code: str) -> str:
    """Translates onboarding copy into the user's locale using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language_code: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to the target language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": "en",  # Assuming source language is English
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
