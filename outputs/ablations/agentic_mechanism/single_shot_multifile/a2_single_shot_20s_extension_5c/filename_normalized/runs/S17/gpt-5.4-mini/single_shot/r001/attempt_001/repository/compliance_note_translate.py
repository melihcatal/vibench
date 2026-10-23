from __future__ import annotations

from typing import Any, Dict

from google.cloud import translate_v3


def compliance_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = "projects/demo-project/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language})
    translated = response.translations[0].translated_text if response.translations else ""
    return {"provider": "google-cloud-translate", "target_language": target_language, "translated_text": translated}
