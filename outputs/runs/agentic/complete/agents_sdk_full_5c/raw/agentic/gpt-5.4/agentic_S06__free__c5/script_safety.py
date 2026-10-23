from __future__ import annotations

from google.cloud import language_v1

from speech_models import SafetyCheckResult


UNSAFE_THRESHOLD = 0.85


def check_script_safety(text: str) -> SafetyCheckResult:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    categories = {
        item.name: item.confidence
        for item in response.moderation_categories
    }
    blocked = any(score >= UNSAFE_THRESHOLD for score in categories.values())
    return SafetyCheckResult(blocked=blocked, categories=categories)
