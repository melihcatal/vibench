import os
from typing import Any, Dict, Optional

from google.cloud import translate_v3 as translate


def translate_payload(payload: Dict[str, Any], target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    def _translate_value(value: Any) -> Any:
        if isinstance(value, str):
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [value],
                    "mime_type": "text/plain",
                    "target_language_code": target_language,
                    **({"source_language_code": source_language} if source_language else {}),
                }
            )
            return response.translations[0].translated_text if response.translations else value
        if isinstance(value, dict):
            return {key: _translate_value(subvalue) for key, subvalue in value.items()}
        if isinstance(value, list):
            return [_translate_value(item) for item in value]
        return value

    return _translate_value(payload)
