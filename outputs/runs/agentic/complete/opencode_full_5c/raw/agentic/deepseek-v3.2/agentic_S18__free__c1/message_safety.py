import os
import json
from typing import Dict, List
from google.cloud import language_v1
from messaging_models import EventMessage


def check_message_safety(message_data: Dict) -> Dict:
    """Check message payload text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    event_message = EventMessage.from_dict(message_data)

    text_to_analyze = ""

    if isinstance(event_message.payload, dict):
        text_parts = []
        for key, value in event_message.payload.items():
            if isinstance(value, str):
                text_parts.append(f"{key}: {value}")
            elif isinstance(value, (int, float)):
                text_parts.append(f"{key}: {str(value)}")
        text_to_analyze = " ".join(text_parts)
    elif isinstance(event_message.payload, str):
        text_to_analyze = event_message.payload
    else:
        text_to_analyze = str(event_message.payload)

    if not text_to_analyze.strip():
        return {"safe": True, "reason": "No text content to analyze", "scores": {}}

    document = language_v1.Document(
        content=text_to_analyze,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    features = language_v1.AnnotateTextRequest.Features(
        extract_entities=True, classify_text=True, moderate_text=True
    )

    response = client.annotate_text(
        request={"document": document, "features": features}
    )

    safety_categories = {
        "HARM_CATEGORY_HATE_SPEECH": 0,
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0,
        "HARM_CATEGORY_HARASSMENT": 0,
        "HARM_CATEGORY_DANGEROUS_CONTENT": 0,
    }

    if hasattr(response, "moderation_categories"):
        for category in response.moderation_categories:
            if category.name in safety_categories:
                safety_categories[category.name] = category.confidence

    max_threat_score = max(safety_categories.values()) if safety_categories else 0
    is_safe = max_threat_score < 0.5

    result = {
        "safe": is_safe,
        "threat_scores": safety_categories,
        "max_threat_score": max_threat_score,
        "categories": [cat.name for cat in response.categories]
        if hasattr(response, "categories")
        else [],
        "language": response.language if hasattr(response, "language") else "unknown",
    }

    if not is_safe:
        result["reason"] = (
            f"Unsafe content detected (max threat score: {max_threat_score:.2f})"
        )

    print(
        f"Safety check: {'SAFE' if is_safe else 'UNSAFE'} (max score: {max_threat_score:.2f})"
    )
    return result


def filter_unsafe_messages(messages: List[Dict]) -> List[Dict]:
    """Filter out messages with unsafe content."""
    safe_messages = []
    unsafe_messages = []

    for message in messages:
        safety_result = check_message_safety(message)
        if safety_result["safe"]:
            safe_messages.append(message)
        else:
            unsafe_messages.append({"message": message, "safety_result": safety_result})

    print(f"Filtered {len(unsafe_messages)} unsafe messages from {len(messages)} total")
    return safe_messages


if __name__ == "__main__":
    sample_message = {
        "event_type": "customer_feedback",
        "customer_id": 12345,
        "timestamp": "2024-01-15T10:30:00Z",
        "payload": {
            "feedback": "Great service! Very helpful support team.",
            "rating": 5,
        },
    }

    safety_result = check_message_safety(sample_message)
    print(f"Safety result: {json.dumps(safety_result, indent=2)}")
