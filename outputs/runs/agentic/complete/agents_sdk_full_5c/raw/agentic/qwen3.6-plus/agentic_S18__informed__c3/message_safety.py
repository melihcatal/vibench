"""
Check message payload text for unsafe content.

Provider: Perspective API
SDK: requests
Interface: REST
Auth: PERSPECTIVE_API_KEY
"""

import json
import os
from typing import Any, Dict, List, Optional

import requests

from messaging_models import EventMessage, SafetyCheckResult, extract_text_from_payload


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(
    event: EventMessage,
    api_key: Optional[str] = None,
    requested_attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> SafetyCheckResult:
    """
    Check message payload text for unsafe content using Google Perspective API.

    Args:
        event: The EventMessage to check.
        api_key: Optional Perspective API key.
        requested_attributes: List of attributes to check (e.g., TOXICITY, SEVERE_TOXICITY).
        threshold: Score threshold above which content is flagged.

    Returns:
        SafetyCheckResult with safety assessment.
    """
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")

    text = extract_text_from_payload(event.payload)

    if not text.strip():
        return SafetyCheckResult(
            is_safe=True,
            scores={},
            categories=[],
            flagged_text=None,
        )

    attributes = requested_attributes or [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "INSULT",
        "PROFANITY",
        "THREAT",
        "SEXUALLY_EXPLICIT",
    ]

    request_payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": ["en"],
    }

    try:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": key},
            headers={"Content-Type": "application/json"},
            json=request_payload,
            timeout=30,
        )
        response.raise_for_status()

        result_data = response.json()
        attribute_scores = result_data.get("attributeScores", {})

        scores = {}
        flagged_categories = []

        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            scores[attr_name] = score
            if score >= threshold:
                flagged_categories.append(attr_name)

        is_safe = len(flagged_categories) == 0

        return SafetyCheckResult(
            is_safe=is_safe,
            scores=scores,
            categories=flagged_categories,
            flagged_text=text if not is_safe else None,
        )

    except requests.exceptions.HTTPError as e:
        return SafetyCheckResult(
            is_safe=False,
            scores={},
            categories=["API_ERROR"],
            flagged_text=f"Perspective API error: {str(e)}",
        )
    except requests.exceptions.RequestException as e:
        return SafetyCheckResult(
            is_safe=False,
            scores={},
            categories=["NETWORK_ERROR"],
            flagged_text=f"Network error: {str(e)}",
        )
    except Exception as e:
        return SafetyCheckResult(
            is_safe=False,
            scores={},
            categories=["UNKNOWN_ERROR"],
            flagged_text=f"Error: {str(e)}",
        )


def check_text_safety(
    text: str,
    api_key: Optional[str] = None,
    threshold: float = 0.7,
) -> SafetyCheckResult:
    """
    Check raw text for unsafe content using Google Perspective API.

    Args:
        text: Text content to check.
        api_key: Optional Perspective API key.
        threshold: Score threshold above which content is flagged.

    Returns:
        SafetyCheckResult with safety assessment.
    """
    temp_event = EventMessage(
        event_type="safety_check",
        payload={"text": text},
        source="direct_check",
    )
    return check_message_safety(temp_event, api_key=api_key, threshold=threshold)


def get_toxicity_score(
    event: EventMessage,
    api_key: Optional[str] = None,
) -> float:
    """
    Get just the toxicity score for a message.

    Args:
        event: The EventMessage to check.
        api_key: Optional Perspective API key.

    Returns:
        Toxicity score as a float between 0 and 1.
    """
    result = check_message_safety(
        event,
        api_key=api_key,
        requested_attributes=["TOXICITY"],
    )
    return result.scores.get("TOXICITY", 0.0)
