import os
from google.cloud import translate


def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    try:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            target_language_code=target_language,
        )
        return response.translations[0].translated_text
    except Exception as e:
        raise Exception(f"Error translating text: {e}")
