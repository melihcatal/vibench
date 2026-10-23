import os
from observability_client import get_translation_client
from google.cloud.translate_v3 import TranslationServiceClient

def translate_log_message(text: str, target_language_code: str, source_language_code: str = "en") -> str:
    translation_client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    parent = f"projects/{project_id}/locations/global"

    response = translation_client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
