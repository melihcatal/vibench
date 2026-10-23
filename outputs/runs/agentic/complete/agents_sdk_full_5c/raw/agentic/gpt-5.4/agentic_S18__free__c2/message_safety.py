from __future__ import annotations

from typing import Any, Dict

from google.cloud import language_v2


PERSPECTIVE_SCOPE_HINT = "Google Cloud Natural Language API"


def check_message_safety(text: str) -> Dict[str, Any]:
    client = language_v2.LanguageServiceClient()
    document = {"content": text, "type_": language_v2.Document.Type.PLAIN_TEXT}
    response = client.moderate_text(request={"document": document})
    scores = {
        item.name: item.confidence
        for item in response.moderation_categories
    }
    unsafe = any(score >= 0.7 for score in scores.values())
    return {
        "provider": PERSPECTIVE_SCOPE_HINT,
        "unsafe": unsafe,
        "scores": scores,
    }
