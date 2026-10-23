import os
import requests
import json
from typing import List, Dict, Any, Optional
from fetch_recent_logs import fetch_recent_logs


def check_log_message_safety(
    text: str, api_key: str = None, attributes: List[str] = None
) -> Dict[str, Any]:
    """
    Check log message text for unsafe content using Perspective API.

    Args:
        text: Text to analyze
        api_key: Perspective API key (defaults to PERSPECTIVE_API_KEY env var)
        attributes: List of attributes to check (TOXICITY, SEVERE_TOXICITY, etc.)

    Returns:
        Dictionary with safety analysis results
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {attr: {} for attr in attributes},
        "doNotStore": True,
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        scores = {}
        for attr in attributes:
            if attr in result.get("attributeScores", {}):
                score = result["attributeScores"][attr]["summaryScore"]["value"]
                scores[attr] = score

        max_score = max(scores.values()) if scores else 0
        max_attribute = max(scores, key=scores.get) if scores else None

        safety_result = {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "scores": scores,
            "max_score": max_score,
            "max_attribute": max_attribute,
            "is_unsafe": max_score > 0.7,
            "risk_level": "HIGH"
            if max_score > 0.7
            else "MEDIUM"
            if max_score > 0.3
            else "LOW",
            "api_used": "Perspective API",
        }

        return safety_result

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "error": str(e),
            "api_used": "Perspective API",
        }


def check_recent_logs_safety(
    hours_back: int = 1, limit: int = 20, threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Check recent log messages for unsafe content using Perspective API.

    Args:
        hours_back: Number of hours to look back
        limit: Maximum number of logs to check
        threshold: Score threshold for marking as unsafe

    Returns:
        List of safety check results
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    logs = fetch_recent_logs(hours_back=hours_back, limit=limit)

    results = []
    unsafe_count = 0

    for log in logs:
        if not log.message or len(log.message.strip()) < 5:
            continue

        safety_result = check_log_message_safety(
            text=log.message,
            api_key=api_key,
            attributes=["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT"],
        )

        result_with_context = {
            **safety_result,
            "timestamp": log.timestamp.isoformat(),
            "severity": log.severity,
            "component": log.labels.get("component", "unknown"),
            "trace_id": log.trace_id,
        }

        results.append(result_with_context)

        if safety_result.get("is_unsafe", False):
            unsafe_count += 1

    print(f"Safety check completed using Perspective API")
    print(f"Checked {len(results)} log messages")
    print(f"Found {unsafe_count} potentially unsafe messages")

    return results


def batch_check_log_safety(
    log_messages: List[str], api_key: str = None
) -> Dict[str, Any]:
    """
    Batch check multiple log messages for safety using Perspective API.

    Args:
        log_messages: List of log messages to check
        api_key: Perspective API key

    Returns:
        Dictionary with batch results
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    all_results = []
    unsafe_messages = []

    for i, message in enumerate(log_messages):
        if not message or len(message.strip()) < 3:
            continue

        try:
            result = check_log_message_safety(message, api_key)
            all_results.append(result)

            if result.get("is_unsafe", False):
                unsafe_messages.append(
                    {
                        "message": message[:200],
                        "score": result["max_score"],
                        "attribute": result["max_attribute"],
                    }
                )

        except Exception as e:
            print(f"Error checking message {i}: {e}")

    summary = {
        "total_checked": len(all_results),
        "unsafe_count": len(unsafe_messages),
        "unsafe_percentage": (len(unsafe_messages) / len(all_results) * 100)
        if all_results
        else 0,
        "average_toxicity_score": sum(
            r.get("scores", {}).get("TOXICITY", 0) for r in all_results
        )
        / len(all_results)
        if all_results
        else 0,
        "unsafe_messages": unsafe_messages[:10],
        "api_used": "Perspective API",
    }

    return {"summary": summary, "detailed_results": all_results[:50]}


if __name__ == "__main__":
    test_messages = [
        "User authentication failed for user admin",
        "System error: Database connection timeout",
        "Warning: Invalid input detected in form submission",
        "This is a test message with no issues",
    ]

    for msg in test_messages:
        result = check_log_message_safety(msg)
        print(f"Message: {msg[:50]}...")
        print(f"  Risk: {result.get('risk_level', 'UNKNOWN')}")
        print(f"  Max score: {result.get('max_score', 0):.3f}")
        print()
