from __future__ import annotations

from typing import Dict, List

from google.cloud import language_v2

from security_models import flatten_label_text, normalize_labels


def check_secret_label_safety(
    labels: Dict[str, str], notes: str = ""
) -> Dict[str, object]:
    client = language_v2.LanguageServiceClient()
    text = flatten_label_text(normalize_labels(labels), notes)
    document = {"content": text, "type_": language_v2.Document.Type.PLAIN_TEXT}
    response = client.moderate_text(request={"document": document})
    flagged_categories: List[str] = [
        item.name for item in response.moderation_categories if item.confidence > 0.5
    ]
    return {
        "provider": "Google Cloud Natural Language API",
        "flagged": bool(flagged_categories),
        "categories": flagged_categories,
        "input_text": text,
    }
