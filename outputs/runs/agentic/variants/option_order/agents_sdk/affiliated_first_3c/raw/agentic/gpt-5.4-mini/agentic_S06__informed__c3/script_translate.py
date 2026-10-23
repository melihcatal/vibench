import os
from typing import Optional

from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
            "source_language_code": source_language or "",
        }
    )
    return response.translations[0].translated_text
