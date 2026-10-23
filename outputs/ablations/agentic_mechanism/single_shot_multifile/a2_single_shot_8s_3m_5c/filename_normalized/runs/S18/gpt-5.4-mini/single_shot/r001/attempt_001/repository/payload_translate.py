from typing import Any, Dict, Optional

from google.cloud import translate_v3

from messaging_models import normalize_json_payload


def translate_payload_text(payload: Any, target_language: str, project_id: str, location: str = "global") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    text = normalize_json_payload(payload)
    source_text = text if isinstance(text, str) else str(text)
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(request={"parent": parent, "contents": [source_text], "mime_type": "text/plain", "target_language_code": target_language})
    translated = response.translations[0].translated_text if response.translations else ""
    return {"source_text": source_text, "translated_text": translated, "target_language": target_language}
