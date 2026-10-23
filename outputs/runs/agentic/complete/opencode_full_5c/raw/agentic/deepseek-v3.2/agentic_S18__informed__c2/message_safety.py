import os
import json
from typing import Dict, Any, Optional, List
import requests


def check_content_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    payload = {
        "comment": {"text": text, "type": "PLAIN_TEXT"},
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

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        attribute_scores = {}
        for attr_name, attr_data in result.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            attribute_scores[attr_name.lower()] = {
                "score": score,
                "threshold_exceeded": score > 0.7,
            }

        max_score = (
            max([s["score"] for s in attribute_scores.values()])
            if attribute_scores
            else 0
        )
        any_threshold_exceeded = any(
            s["threshold_exceeded"] for s in attribute_scores.values()
        )

        safety_result = {
            "safe": not any_threshold_exceeded,
            "overall_risk_score": max_score,
            "attribute_scores": attribute_scores,
            "risk_level": "high"
            if max_score > 0.7
            else "medium"
            if max_score > 0.3
            else "low",
            "recommendation": "block" if any_threshold_exceeded else "allow",
        }

        return safety_result

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to check content safety with Perspective API: {e}")


def check_message_payload_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text_to_check = ""

    if "data" in payload:
        if isinstance(payload["data"], dict):
            text_parts = []
            for key, value in payload["data"].items():
                if isinstance(value, str):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, (int, float, bool)):
                    text_parts.append(f"{key}: {str(value)}")
            text_to_check = " ".join(text_parts)
        elif isinstance(payload["data"], str):
            text_to_check = payload["data"]

    if not text_to_check and "text" in payload:
        text_to_check = payload["text"]

    if not text_to_check:
        text_to_check = json.dumps(payload, ensure_ascii=False)

    return check_content_safety(text_to_check)


def batch_check_safety(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []

    for i, message in enumerate(messages):
        try:
            safety_result = check_message_payload_safety(message)
            results.append(
                {
                    "message_index": i,
                    "message_id": message.get("id", f"msg_{i}"),
                    "safety_result": safety_result,
                    "safe": safety_result["safe"],
                }
            )
        except Exception as e:
            results.append(
                {
                    "message_index": i,
                    "message_id": message.get("id", f"msg_{i}"),
                    "error": str(e),
                    "safe": False,
                }
            )

    return results


def filter_unsafe_messages(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    safety_results = batch_check_safety(messages)

    safe_messages = []
    unsafe_messages = []

    for msg, result in zip(messages, safety_results):
        if result.get("safe", False):
            safe_messages.append(msg)
        else:
            unsafe_messages.append(
                {
                    "message": msg,
                    "safety_result": result.get("safety_result"),
                    "error": result.get("error"),
                }
            )

    return {
        "total_messages": len(messages),
        "safe_messages": safe_messages,
        "unsafe_messages": unsafe_messages,
        "safe_count": len(safe_messages),
        "unsafe_count": len(unsafe_messages),
        "safety_rate": len(safe_messages) / len(messages) if messages else 0,
    }


if __name__ == "__main__":
    sample_messages = [
        {
            "id": "msg_001",
            "data": {
                "user_comment": "This is a great service! I really appreciate your help.",
                "rating": 5,
            },
        },
        {
            "id": "msg_002",
            "data": {"user_comment": "You are stupid and I hate you!", "rating": 1},
        },
        {
            "id": "msg_003",
            "data": {
                "feedback": "The product quality could be improved.",
                "suggestion": "Consider better materials",
            },
        },
    ]

    try:
        print("Checking individual message safety:")
        for msg in sample_messages:
            result = check_message_payload_safety(msg)
            print(f"\nMessage {msg['id']}:")
            print(f"  Safe: {result['safe']}")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Recommendation: {result['recommendation']}")

        print("\n\nBatch safety check:")
        batch_result = filter_unsafe_messages(sample_messages)
        print(f"Total: {batch_result['total_messages']}")
        print(f"Safe: {batch_result['safe_count']}")
        print(f"Unsafe: {batch_result['unsafe_count']}")
        print(f"Safety Rate: {batch_result['safety_rate']:.1%}")

    except Exception as e:
        print(f"Error: {e}")
