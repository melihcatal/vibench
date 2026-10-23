# profile_moderation.py - Moderate profile text before account activation
# Using Azure AI Content Safety as the concrete provider

import os
import requests
import json
from typing import TypedDict

CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

CONTENT_SAFETY_URL = f"{CONTENT_SAFETY_ENDPOINT}/v1.0/text/moderations/content"


class ModerationResponse(TypedDict):
    flagged: bool
    category: str
    severity: str
    details: Dict[str, str]


def moderate_profile_text(text: str) -> ModerationResponse:
    """Submit user supplied profile text to Azure Content Safety and return moderation result.",

    Returns a dict indicating whether the text is flagged, the content category,
    the severity level, and any detail fields provided by the service.",
    """
    payload = {
        "content": text,
        "content_type": "text/plain",
        "model": "default",
        "custom_words": [],  # can be extended for domain-specific vocab
    }
    headers = {"api-key": CONTENT_SAFETY_KEY, "Content-Type": "application/json"}
    resp = requests.post(CONTENT_SAFETY_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    # Azure returns a list; we take the first (and typically only) moderation result
    result = data[0]
    return {
        "flagged": result["flags"] != [],
        "category": result["category"],
        "severity": result["severity"],
        "details": result.get("details", {}),
    }
