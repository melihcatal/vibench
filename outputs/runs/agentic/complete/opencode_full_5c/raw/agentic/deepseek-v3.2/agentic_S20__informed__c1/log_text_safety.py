import os
import json
from typing import Dict, Any, List, Optional
import requests


def check_log_message_safety(log_message: str, language: str = "en") -> Dict[str, Any]:
    """Check selected log message text for unsafe content using Perspective API."""

    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    # Perspective API endpoint
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Prepare request payload
    payload = {
        "comment": {"text": log_message},
        "languages": [language],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    params = {"key": api_key}

    try:
        # Make API request
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract attribute scores
        attribute_scores = result.get("attributeScores", {})

        # Calculate overall safety score (average of all attributes)
        scores = []
        safety_details = {}

        for attribute_name, attribute_data in attribute_scores.items():
            score = attribute_data.get("summaryScore", {}).get("value", 0)
            scores.append(score)
            safety_details[attribute_name.lower()] = {
                "score": score,
                "threshold_exceeded": score > 0.7,  # Common threshold for moderation
            }

        overall_score = sum(scores) / len(scores) if scores else 0

        # Determine safety status
        if overall_score > 0.8:
            safety_status = "UNSAFE"
            action_recommended = "REDACT_OR_REVIEW"
        elif overall_score > 0.5:
            safety_status = "SUSPICIOUS"
            action_recommended = "REVIEW"
        else:
            safety_status = "SAFE"
            action_recommended = "NO_ACTION"

        # Check for any high-risk attributes
        high_risk_attributes = []
        for attr_name, attr_info in safety_details.items():
            if attr_info["score"] > 0.8:
                high_risk_attributes.append(attr_name)

        return {
            "safety_check": {
                "status": safety_status,
                "overall_score": overall_score,
                "action_recommended": action_recommended,
                "high_risk_attributes": high_risk_attributes,
            },
            "detailed_scores": safety_details,
            "metadata": {
                "message_length": len(log_message),
                "language": language,
                "provider": "Perspective API",
                "model": "Perspective API toxicity detection",
            },
        }

    except requests.exceptions.RequestException as e:
        # Fallback for API errors
        return {
            "safety_check": {
                "status": "CHECK_FAILED",
                "overall_score": None,
                "action_recommended": "MANUAL_REVIEW",
                "high_risk_attributes": [],
                "error": str(e),
            },
            "detailed_scores": {},
            "metadata": {
                "message_length": len(log_message),
                "language": language,
                "provider": "Perspective API",
                "error": f"API request failed: {str(e)}",
            },
        }


def check_logs_safety_batch(
    log_messages: List[str], language: str = "en"
) -> Dict[str, Any]:
    """Check multiple log messages for safety in batch."""

    results = []
    unsafe_count = 0
    suspicious_count = 0

    for i, message in enumerate(log_messages):
        result = check_log_message_safety(message, language)
        results.append(
            {
                "index": i,
                "message_preview": message[:100]
                + ("..." if len(message) > 100 else ""),
                "safety_result": result["safety_check"],
                "detailed_scores": result.get("detailed_scores", {}),
            }
        )

        if result["safety_check"]["status"] == "UNSAFE":
            unsafe_count += 1
        elif result["safety_check"]["status"] == "SUSPICIOUS":
            suspicious_count += 1

    # Summary statistics
    total_messages = len(log_messages)
    safe_count = total_messages - unsafe_count - suspicious_count

    return {
        "batch_summary": {
            "total_messages_checked": total_messages,
            "safe_messages": safe_count,
            "suspicious_messages": suspicious_count,
            "unsafe_messages": unsafe_count,
            "unsafe_percentage": (unsafe_count / total_messages * 100)
            if total_messages > 0
            else 0,
        },
        "detailed_results": results,
        "recommendations": {
            "redact_unsafe": unsafe_count > 0,
            "review_suspicious": suspicious_count > 0,
            "action_required": unsafe_count > 0 or suspicious_count > 0,
        },
    }


def redact_unsafe_content(log_message: str, safety_result: Dict[str, Any]) -> str:
    """Redact unsafe content from log message based on safety check."""

    if safety_result.get("status") != "UNSAFE":
        return log_message

    # Simple redaction - replace with placeholder
    # In production, you might want more sophisticated redaction
    redacted_message = "[REDACTED: UNSAFE_CONTENT]"

    # Keep some context if possible (first 50 chars)
    if len(log_message) > 50:
        preview = log_message[:50]
        redacted_message = f"{preview}... [REDACTED: UNSAFE_CONTENT]"

    return redacted_message


if __name__ == "__main__":
    # Example usage
    test_message = "This is a test log message with potentially toxic content."

    result = check_log_message_safety(test_message)
    print("Safety Check Result:")
    print(json.dumps(result, indent=2))

    # Batch example
    test_messages = [
        "Normal log message about user login",
        "Error: Database connection failed",
        "Warning: Invalid input from user",
        "This contains inappropriate language that should be filtered",
    ]

    batch_result = check_logs_safety_batch(test_messages)
    print("\nBatch Safety Check:")
    print(json.dumps(batch_result["batch_summary"], indent=2))
