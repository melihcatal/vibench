"""
[LATER-STEP] Check message payload text for unsafe content using Azure AI Content Safety.
Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import json
from typing import Dict, Any, Optional, List
from messaging_models import PubSubEvent, extract_text_from_event


def check_message_safety(
    text: str,
    endpoint: str = None,
    api_key: str = None,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check text content for unsafe categories using Azure AI Content Safety API.

    Args:
        text: The text content to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.
        categories: List of categories to check (default: all four).

    Returns:
        Dictionary with safety analysis results per category.
    """
    import requests

    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    result = response.json()

    analysis = {
        "is_safe": True,
        "categories": {},
        "raw_response": result,
    }

    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        analysis["categories"][cat_name] = {
            "severity": severity,
            "flagged": severity > 0,
        }
        if severity > 0:
            analysis["is_safe"] = False

    return analysis


def check_event_safety(
    event: PubSubEvent,
    endpoint: str = None,
    api_key: str = None,
) -> Dict[str, Any]:
    """
    Check a PubSubEvent's text content for safety issues.

    Args:
        event: The PubSubEvent to check.

    Returns:
        Safety analysis dictionary.
    """
    text = extract_text_from_event(event)
    return check_message_safety(text, endpoint=endpoint, api_key=api_key)


def check_batch_safety(
    events: List[PubSubEvent],
    endpoint: str = None,
    api_key: str = None,
) -> List[Dict[str, Any]]:
    """
    Check multiple events for safety issues.

    Args:
        events: List of PubSubEvent objects.

    Returns:
        List of safety analysis dictionaries.
    """
    results = []
    for event in events:
        result = check_event_safety(event, endpoint=endpoint, api_key=api_key)
        result["event_id"] = event.event_id
        results.append(result)
    return results
