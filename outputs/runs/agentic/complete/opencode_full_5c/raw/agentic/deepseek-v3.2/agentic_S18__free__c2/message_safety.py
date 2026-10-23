import os
from typing import Dict, Any, List
from google.cloud import language_v1
import json


def check_message_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Check message payload text for unsafe content using Google Cloud Natural Language API."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    client = language_v1.LanguageServiceClient()

    text_content = extract_text_from_payload(payload)

    if not text_content:
        return {"safe": True, "reason": "No text content to analyze", "scores": {}}

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    safety_result = {
        "safe": True,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "categories": [],
        "flagged_terms": [],
    }

    if response.document_sentiment.score < -0.5:
        safety_result["safe"] = False
        safety_result["categories"].append("highly_negative_sentiment")

    if response.document_sentiment.magnitude > 2.0:
        safety_result["categories"].append("high_emotional_intensity")

    unsafe_terms = check_for_unsafe_terms(text_content)
    if unsafe_terms:
        safety_result["safe"] = False
        safety_result["flagged_terms"] = unsafe_terms

    return safety_result


def extract_text_from_payload(payload: Dict[str, Any]) -> str:
    """Extract text content from message payload."""
    text_parts = []

    for key, value in payload.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            text_parts.append(value)
        elif isinstance(value, dict):
            nested_text = extract_text_from_payload(value)
            if nested_text:
                text_parts.append(nested_text)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    text_parts.append(item)
                elif isinstance(item, dict):
                    nested_text = extract_text_from_payload(item)
                    if nested_text:
                        text_parts.append(nested_text)

    return " ".join(text_parts)


def check_for_unsafe_terms(text: str) -> List[str]:
    """Check for unsafe terms in text (simplified version)."""
    unsafe_patterns = [
        "hack",
        "exploit",
        "ddos",
        "phishing",
        "malware",
        "password",
        "credit card",
        "ssn",
        "social security",
    ]

    found_terms = []
    text_lower = text.lower()

    for pattern in unsafe_patterns:
        if pattern in text_lower:
            found_terms.append(pattern)

    return found_terms


if __name__ == "__main__":
    sample_payload = {
        "message": "Your account has been compromised. Please reset your password immediately.",
        "user_id": "user_123",
        "action": "security_alert",
    }

    try:
        safety_check = check_message_safety(sample_payload)
        print("Message Safety Check:")
        print(json.dumps(safety_check, indent=2))
    except Exception as e:
        print(f"Failed to check message safety: {e}")
