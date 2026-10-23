from __future__ import annotations

from typing import Dict

from observability_client import load_config, translate_client
from observability_models import DashboardNoteTranslateRequest


def dashboard_note_translate(request: DashboardNoteTranslateRequest) -> Dict[str, str]:
    config = load_config()
    client = translate_client()
    parent = config.translate_parent
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "mime_type": "text/plain",
            "target_language_code": request.target_language_code,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"source": request.text, "translated": translated, "target_language_code": request.target_language_code}
