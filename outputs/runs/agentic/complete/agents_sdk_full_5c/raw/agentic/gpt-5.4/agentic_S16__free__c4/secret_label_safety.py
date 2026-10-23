from __future__ import annotations

from typing import Dict, List

from google.cloud import language_v2

from security_models import normalize_labels, safe_text

UNSAFE_CATEGORIES = {"toxic", "insult", "profanity", "derogatory"}


def check_secret_label_safety(labels: Dict[str, str], notes: str = "") -> dict:
    client = language_v2.LanguageServiceClient()
    normalized = normalize_labels(labels)
    combined = "\n".join([f"{k}:{v}" for k, v in normalized.items()] + [safe_text(notes)])
    document = {"content": combined, "type_": language_v2.Document.Type.PLAIN_TEXT}
    response = client.moderate_text(request={"document": document})
    flagged: List[dict] = []
    for moderation in response.moderation_categories:
        name = moderation.name.lower()
        if any(category in name for category in UNSAFE_CATEGORIES):
            flagged.append({"category": moderation.name, "confidence": moderation.confidence})
    return {"safe": len(flagged) == 0, "flagged": flagged, "provider": "google-cloud-language-v2"}
