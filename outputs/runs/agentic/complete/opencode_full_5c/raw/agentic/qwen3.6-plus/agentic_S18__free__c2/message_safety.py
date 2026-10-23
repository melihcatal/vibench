import os
import json
from typing import Any

from google.cloud import language_v2
from google.cloud.language_v2.types import (
    AnalyzeModerationTextRequest,
    ModerationCategory,
)

from messaging_models import PubSubEvent


GOOGLE_CLOUD_PROJECT_ENV = "GCP_PROJECT_ID"
SAFETY_CONFIDENCE_THRESHOLD = 0.5


def _get_language_client() -> language_v2.LanguageServiceClient:
    return language_v2.LanguageServiceClient()


def check_message_safety(
    text: str,
    confidence_threshold: float = SAFETY_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    client = _get_language_client()
    project_id = os.environ.get(GOOGLE_CLOUD_PROJECT_ENV, "default-project")

    document = language_v2.types.Document(
        content=text,
        type_=language_v2.types.Document.Type.PLAIN_TEXT,
    )

    request = AnalyzeModerationTextRequest(
        document=document,
    )

    response = client.analyze_moderation_text(request=request)

    flagged_categories = []
    is_safe = True

    for category in response.moderation_categories:
        if category.confidence >= confidence_threshold:
            is_safe = False
            flagged_categories.append(
                {
                    "category": ModerationCategory(category.category).name
                    if hasattr(ModerationCategory, category.category)
                    else str(category.category),
                    "confidence": category.confidence,
                    "category_name": category.category_name,
                }
            )

    return {
        "is_safe": is_safe,
        "flagged_categories": flagged_categories,
        "confidence_threshold": confidence_threshold,
        "model_used": "google-cloud-language-v2",
        "text_length": len(text),
    }


def check_event_payload_safety(
    event: PubSubEvent,
    confidence_threshold: float = SAFETY_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    payload_text = json.dumps(event.payload, default=str)
    safety_result = check_message_safety(payload_text, confidence_threshold)
    safety_result["event_id"] = event.event_id
    safety_result["event_type"] = event.event_type
    return safety_result


def sanitize_payload_if_unsafe(
    event: PubSubEvent,
    confidence_threshold: float = SAFETY_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    safety_result = check_event_payload_safety(event, confidence_threshold)

    if safety_result["is_safe"]:
        return {
            "event_id": event.event_id,
            "action": "approved",
            "safety_result": safety_result,
        }

    return {
        "event_id": event.event_id,
        "action": "quarantined",
        "safety_result": safety_result,
        "original_payload": event.payload,
        "quarantine_reason": "content_failed_safety_check",
    }


if __name__ == "__main__":
    sample_text = "This is a normal customer message about order #12345."
    result = check_message_safety(sample_text)
    print(json.dumps(result, indent=2))
