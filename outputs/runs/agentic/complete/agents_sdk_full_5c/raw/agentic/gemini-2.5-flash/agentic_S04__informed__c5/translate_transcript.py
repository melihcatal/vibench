import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str = "es", project_id: str = None) -> str:
    """Translates text using Google Cloud Translation."""
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided or GOOGLE_CLOUD_PROJECT env var not set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, we'll take the first one.
    if response.translations:
        return response.translations[0].translated_text
    return ""
