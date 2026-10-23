import os
import json
from typing import Dict, Any, List, Optional
import requests
from dataclasses import dataclass


@dataclass
class SafetyScore:
    """Safety scoring results."""

    toxicity: float
    severe_toxicity: float
    identity_attack: float
    insult: float
    threat: float
    sexually_explicit: float
    overall_risk: str

    @classmethod
    def from_perspective_response(cls, response_data: Dict[str, Any]) -> "SafetyScore":
        """Create SafetyScore from Perspective API response."""
        attribute_scores = response_data.get("attributeScores", {})

        toxicity = (
            attribute_scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
        )
        severe_toxicity = (
            attribute_scores.get("SEVERE_TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0)
        )
        identity_attack = (
            attribute_scores.get("IDENTITY_ATTACK", {})
            .get("summaryScore", {})
            .get("value", 0)
        )
        insult = (
            attribute_scores.get("INSULT", {}).get("summaryScore", {}).get("value", 0)
        )
        threat = (
            attribute_scores.get("THREAT", {}).get("summaryScore", {}).get("value", 0)
        )
        sexually_explicit = (
            attribute_scores.get("SEXUALLY_EXPLICIT", {})
            .get("summaryScore", {})
            .get("value", 0)
        )

        max_score = max(
            toxicity,
            severe_toxicity,
            identity_attack,
            insult,
            threat,
            sexually_explicit,
        )

        if max_score >= 0.8:
            overall_risk = "HIGH"
        elif max_score >= 0.5:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"

        return cls(
            toxicity=toxicity,
            severe_toxicity=severe_toxicity,
            identity_attack=identity_attack,
            insult=insult,
            threat=threat,
            sexually_explicit=sexually_explicit,
            overall_risk=overall_risk,
        )


def check_log_message_safety(
    message: str, languages: List[str] = None
) -> Dict[str, Any]:
    """Check selected log message text for unsafe content using Perspective API."""
    if languages is None:
        languages = ["en"]

    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    request_body = {
        "comment": {"text": message},
        "languages": languages,
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "doNotStore": True,
    }

    try:
        response = requests.post(url, params=params, json=request_body)
        response.raise_for_status()

        response_data = response.json()

        safety_score = SafetyScore.from_perspective_response(response_data)

        result = {
            "message_preview": message[:100] + ("..." if len(message) > 100 else ""),
            "safety_score": {
                "toxicity": safety_score.toxicity,
                "severe_toxicity": safety_score.severe_toxicity,
                "identity_attack": safety_score.identity_attack,
                "insult": safety_score.insult,
                "threat": safety_score.threat,
                "sexually_explicit": safety_score.sexually_explicit,
                "overall_risk": safety_score.overall_risk,
            },
            "is_safe": safety_score.overall_risk == "LOW",
            "recommendation": "No action needed"
            if safety_score.overall_risk == "LOW"
            else "Review recommended",
        }

        print(f"Safety check completed. Overall risk: {safety_score.overall_risk}")

        return result

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        raise
    except Exception as e:
        print(f"Error processing safety check: {e}")
        raise


def check_multiple_log_messages(messages: List[str]) -> List[Dict[str, Any]]:
    """Check multiple log messages for safety."""
    results = []

    for i, message in enumerate(messages):
        try:
            result = check_log_message_safety(message)
            result["message_index"] = i
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "message_index": i,
                    "message_preview": message[:100]
                    + ("..." if len(message) > 100 else ""),
                    "error": str(e),
                    "is_safe": None,
                }
            )

    unsafe_count = sum(1 for r in results if r.get("is_safe") is False)
    print(
        f"Checked {len(messages)} messages. Found {unsafe_count} potentially unsafe messages."
    )

    return results


if __name__ == "__main__":
    test_messages = [
        "User authentication failed for user_id: 12345",
        "System error: Database connection timeout",
        "This is a test message with no issues",
        "Warning: High memory usage detected",
        "Error: Payment processing failed for transaction ABC123",
    ]

    print("Testing log message safety check with Perspective API...")

    try:
        results = check_multiple_log_messages(test_messages)

        for result in results:
            print(f"\nMessage {result.get('message_index')}:")
            print(f"  Preview: {result.get('message_preview')}")
            if "safety_score" in result:
                print(f"  Overall risk: {result['safety_score']['overall_risk']}")
                print(f"  Is safe: {result['is_safe']}")
            else:
                print(f"  Error: {result.get('error')}")

    except Exception as e:
        print(f"Test failed: {e}")
        print(
            "Note: PERSPECTIVE_API_KEY environment variable must be set for this test"
        )
