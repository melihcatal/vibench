import os
from google.cloud import translate_v3
from security_models import TranslationResult

def translate_runbook_notes(text: str, target_language_code: str, source_language_code: str = "en", project_id: str = None) -> TranslationResult:
    if project_id is None:
        project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID not provided and not found in environment variables.")

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            translated_text = response.translations[0].translated_text
            return TranslationResult(
                translated_text=translated_text,
                source_language_code=source_language_code,
                target_language_code=target_language_code
            )
        raise RuntimeError("No translation returned.")

    except Exception as e:
        raise RuntimeError(f"Error translating runbook notes with Google Cloud Translation: {e}")
