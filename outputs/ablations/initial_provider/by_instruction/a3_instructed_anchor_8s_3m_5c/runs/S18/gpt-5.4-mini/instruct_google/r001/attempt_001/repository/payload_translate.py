from typing import Any, Dict

from google.cloud import translate_v3


def translate_payload_text(text: str, target_language: str, project_id: str, location: str = "global") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    translation = response.translations[0]
    return {"translated_text": translation.translated_text, "detected_language_code": translation.detected_language_code}
