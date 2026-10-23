from google.cloud import translate
import os

def translate_runbook_notes(text: str, target_language: str, project_id: str) -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation."
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    # The GOOGLE_CLOUD_PROJECT environment variable should be set for the project_id
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text
