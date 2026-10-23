# [LATER-STEP] corpus_safety.py
# Check corpus text before embedding

# Provider: Azure AI Content Safety (REST API) – identifiable via endpoint and key
# Integration signal: AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables

import os
import requests
from typing import Tuple

CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

if not (CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY):
    raise RuntimeError(
        "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables"
    )


def check_corpus_safety(text: str) -> Tuple[bool, dict]:
    """Check text for policy violations using Azure Content Safety.
    Returns (is_safe, details) where is_safe is a boolean.
    """
    url = f"{CONTENT_SAFETY_ENDPOINT}/contentSafety/chat/moderations?api-version=2023-05-01"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
    }
    payload = {
        "input": {
            "text": text,
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    data = resp.json()
    # Simplified extraction – assume first moderation result
    result = data.get("results", [{}])[0]
    flagged = any(item.get("flagged", False) for item in result.get("categories", []))
    return not flagged, data  # not flagged => safe
