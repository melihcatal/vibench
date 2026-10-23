from typing import Optional

from google.cloud import translate
from storage_models import StoredTextTranslatePayload
import os

def stored_text_translate(payload: StoredTextTranslatePayload, config: Optional[StorageConfig] = None) -> dict:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if config and config.project_id:
        project_id = config.project_id
    
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided in config or GOOGLE_CLOUD_PROJECT environment variable.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload.text],
            "source_language_code": payload.source_language_code,
            "target_language_code": payload.target_language_code,
            "mime_type": "text/plain",
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    return {"translated_text": translations[0] if translations else ""}
