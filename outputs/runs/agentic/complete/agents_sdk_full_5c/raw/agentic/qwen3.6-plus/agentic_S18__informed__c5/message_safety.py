"""Check message payload text for unsafe content using Azure AI Content Safety.

Uses the Azure AI Content Safety REST API to analyze text payloads for
hate, self-harm, sexual, and violence content. Authentication relies on
AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.
"""

import os
import json
from typing import Dict, List, Optional

import requests

from messaging_models import ConsumedMessage


CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.cognitiveservices.azure.com/"
)
CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

# Azure AI Content Safety API version
API_VERSION = "2024-02-15-preview"
CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


def check_text_safety(text: str) -> Dict[str, float]:
    """Send text to Azure AI Content Safety for moderation analysis.

    Args:
        text: The raw text to scan.

    Returns:
        Dict mapping each category to its severity score (0-7).
    """
    url = (
        f"{CONTENT_SAFETY_ENDPOINT.rstrip('/')}"
        f"/contentsafety/text:analyze?api-version={API_VERSION}"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "output_type": "EightSeverityLevels",
        "categories": CATEGORIES,
    }

    response = requests.post(url, headers=headers, json=body, timeout=15)
    response.raise_for_status()

    result = response.json()
    severity_scores: Dict[str, float] = {}
    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "")
        sev = category_result.get("severity", 0)
        severity_scores[cat_name] = sev

    return severity_scores


def check_message_safety(
    message: ConsumedMessage,
    text_fields: Optional[List[str]] = None,
    threshold: float = 3.0,
) -> List[str]:
    """Analyze a ConsumedMessage payload for unsafe content.

    Extracts text from the specified fields (defaults to all string
    values in the payload) and checks each against Azure AI Content Safety.

    Args:
        message: The consumed message to inspect.
        text_fields: Optional list of payload keys to scan.
        threshold: Severity level above which a flag is raised.

    Returns:
        List of flagged category names (e.g. ["Hate", "Violence"]).
    """
    payload = message.payload
    if not text_fields:
        text_fields = [k for k, v in payload.items() if isinstance(v, str)]

    all_scores: Dict[str, float] = {}
    for field_name in text_fields:
        field_text = payload.get(field_name, "")
        if not field_text:
            continue
        scores = check_text_safety(str(field_text))
        for cat, sev in scores.items():
            all_scores[cat] = max(all_scores.get(cat, 0.0), sev)

    flagged = [cat for cat, sev in all_scores.items() if sev >= threshold]
    return flagged


if __name__ == "__main__":
    sample = ConsumedMessage(
        message_id="msg-check-1",
        event_id="evt-001",
        event_type="comment.posted",
        source="social-api",
        payload={"comment": "This is a perfectly normal message.", "author": "bob"},
        attributes={},
    )
    flags = check_message_safety(sample)
    print(json.dumps({"flags": flags}))
