from typing import Dict, List
from safety_client import SafetyClient
from safety_models import ModerationCategory, RedactionResult


def redact_unsafe(text: str) -> Dict:
    client = SafetyClient()
    thresholds = {
        ModerationCategory.HATE_SPEECH: 0.7,
        ModerationCategory.DANGEROUS_CONTENT: 0.8,
        ModerationCategory.HARASSMENT: 0.75,
        ModerationCategory.SEXUALLY_EXPLICIT: 0.8,
    }

    moderation_data = client.moderate_text_content(text)
    if not moderation_data:
        return {
            "redacted_text": text,
            "unsafe_spans": [],
            "flagged_categories": ["moderation_failed"],
        }

    moderation_scores = moderation_data["moderation_scores"]
    flagged_categories = []
    for category, threshold in thresholds.items():
        if moderation_scores[category.value] >= threshold:
            flagged_categories.append(category)

    # Simulate redaction by replacing unsafe spans with [REDACTED]
    # In a real implementation, this would use the API's span detection
    unsafe_spans = []
    redacted_text = text
    if flagged_categories:
        redacted_text = "[REDACTED]"
        unsafe_spans = [{"start": 0, "end": len(text)}]

    return {
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
        "flagged_categories": [cat.value for cat in flagged_categories],
    }
