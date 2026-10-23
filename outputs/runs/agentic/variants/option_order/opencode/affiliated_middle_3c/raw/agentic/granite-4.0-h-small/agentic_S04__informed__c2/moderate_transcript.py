import os
from typing import List, Dict

# Moderation utilities using Watsonx Guardrails API (IBM)

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError("WATSONX_API_KEY or WATSONX_PROJECT_ID not set")

BASE_URL = "https://api.ibm.com/watsonx/v1"

import requests


def moderate_transcript(transcript_segments: List[str]) -> List[Dict]:
    """Call Watsonx Content Moderation endpoint for each segment."""
    url = f"{BASE_URL}/moderation/v1/text"
    headers = {
        "Authorization": f"Bearer {WATSONX_API_KEY}",
        "Content-Type": "application/json",
    }
    payloads = []
    for seg in transcript_segments:
        payloads.append({"text": seg, "moderation_type": "content"})
    # Batch request (if API supports batch, otherwise iterate)
    resp = requests.post(
        url, json={"text": "\n".join(transcript_segments)}, headers=headers
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    moderated = []
    for r in results:
        moderated.append(
            {"segment": r.get("text"), "moderation": r.get("moderations", [{}])[0]}
        )
    return moderated


# Simple helper to filter out disallowed content


def filter_allowed(moderated: List[Dict]) -> List[str]:
    allowed = []
    for item in moderated:
        # Assume 'label' with value 'allowed' means safe
        if item.get("moderation", {}).get("label") == "allowed":
            allowed.append(item.get("segment"))
    return allowed
