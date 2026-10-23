"""Check message payload text for unsafe content using OpenAI Moderation API.

Scans message payloads for unsafe content categories including
hate, self-harm, sexual, violence, and other policy violations.
"""

import json
from typing import Dict, Any, List, Optional

from openai import OpenAI

from messaging_models import ConsumedMessage, normalize_payload

_OPENAI_MODEL_ID = "text-moderation-latest"


def check_message_safety(
    message: ConsumedMessage,
) -> Dict[str, Any]:
    """Check a consumed message payload for unsafe content using OpenAI.

    Args:
        message: ConsumedMessage to check.

    Returns:
        Dictionary with safety flags, flagged categories, and risk score.
    """
    payload = normalize_payload(message.payload)
    text_content = _extract_text_from_payload(payload)

    if not text_content:
        return {
            "message_id": message.message_id,
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "risk_score": 0.0,
            "safe": True,
        }

    client = OpenAI()
    moderation = client.moderations.create(
        input=text_content,
        model=_OPENAI_MODEL_ID,
    )

    result = moderation.results[0]
    category_scores = {}
    categories = {}

    for cat_name, flagged in result.categories.__dict__.items():
        categories[cat_name] = bool(flagged)

    for cat_name, score in result.category_scores.__dict__.items():
        if isinstance(score, (int, float)):
            category_scores[cat_name] = float(score)

    risk_score = max(category_scores.values()) if category_scores else 0.0

    return {
        "message_id": message.message_id,
        "event_id": message.event_id,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "risk_score": round(risk_score, 4),
        "safe": not result.flagged,
    }


def batch_check_safety(
    messages: List[ConsumedMessage],
) -> List[Dict[str, Any]]:
    """Batch check multiple messages for unsafe content using OpenAI.

    Args:
        messages: List of ConsumedMessage objects to check.

    Returns:
        List of safety check results.
    """
    results = []
    for msg in messages:
        safety_result = check_message_safety(msg)
        results.append(safety_result)
    return results


def is_message_safe(
    message: ConsumedMessage,
    max_risk_score: float = 0.5,
) -> bool:
    """Quick check if a message is safe for processing.

    Args:
        message: ConsumedMessage to check.
        max_risk_score: Maximum acceptable risk score.

    Returns:
        True if message is safe, False otherwise.
    """
    safety_result = check_message_safety(message)
    return safety_result["safe"] and safety_result["risk_score"] <= max_risk_score


def _extract_text_from_payload(payload: Dict[str, Any]) -> str:
    """Extract text content from a normalized payload.

    Args:
        payload: Normalized payload dictionary.

    Returns:
        Extracted text string.
    """
    text_parts = []

    for key in ["text", "message", "content", "body", "description"]:
        if key in payload and isinstance(payload[key], str):
            text_parts.append(payload[key])

    if not text_parts:
        text_parts.append(json.dumps(payload, default=str))

    return " ".join(text_parts)
