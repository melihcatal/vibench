from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import translate_v3


def translate_compliance_note(text: str, target_language: str = "en", project_id: str | None = None, location: str = "global") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}" if project_id else f"projects/-/locations/{location}"
    response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language})
    translated = response.translations[0].translated_text if response.translations else ""
    return {"provider": "google-cloud-translate", "translated_text": translated, "target_language": target_language}


def main() -> Dict[str, Any]:
    text = os.environ.get("COMPLIANCE_NOTE", "")
    target_language = os.environ.get("TARGET_LANGUAGE", "en")
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    return translate_compliance_note(text=text, target_language=target_language, project_id=project_id)
