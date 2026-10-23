import os
from google.cloud import translate_v3 as translate

def record_translate(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translate user-facing document fields using Google Cloud Translation.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    """
    client = translate.TranslationServiceClient()

    # The location must be a global location (e.g., "global") or a regional location (e.g., "us-central1").
    # For this example, we use "global".
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # For the purposes of this example, we assume a single text input
    if response.translations:
        return response.translations[0].translated_text
    return text # Return original text if no translation occurs
