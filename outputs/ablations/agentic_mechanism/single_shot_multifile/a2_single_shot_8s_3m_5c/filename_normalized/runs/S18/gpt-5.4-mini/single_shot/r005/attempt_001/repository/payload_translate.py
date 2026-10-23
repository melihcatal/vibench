import os
from typing import Any, Dict

from google.cloud import translate_v3


def translate_payload_text(text: str, target_language: str) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    translated = response.translations[0].translated_text if response.translations else text
    return {"provider": "google-cloud-translate-v3", "translated_text": translated, "target_language": target_language}
