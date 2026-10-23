from __future__ import annotations

import os

from google.cloud import language_v2

from messaging_models import normalize_text_payload


GOOGLE_LANGUAGE_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")


def check_message_safety(payload: dict) -> dict[str, object]:
    text = normalize_text_payload(payload)
    client = language_v2.LanguageServiceClient()
    document = {"content": text, "type_": language_v2.Document.Type.PLAIN_TEXT}
    response = client.moderate_text(document=document)
    categories = [
        {"name": category.name, "confidence": float(category.confidence)}
        for category in response.moderation_categories
    ]
    flagged = any(category["confidence"] >= 0.5 for category in categories)
    return {
        "provider": "google-cloud-natural-language",
        "location": GOOGLE_LANGUAGE_LOCATION,
        "flagged": flagged,
        "categories": categories,
    }
