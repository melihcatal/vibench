# moderate_text.py
"""Scores user text for unsafe or policy-violating content (Azure AI Content Safety)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import Dict, Any

# Azure AI Content Safety uses a subscription key for authentication
# AZURE_CONTENT_SAFETY_KEY is set in the environment


def moderate_text(text: str, categories: list[str]) -> Dict[str, Any]:
    """Send a single piece of user text to Azure moderation and return normalized results."""
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    payload = build_api_request(text, categories)
    # Simple REST call using requests (provider-specific import shown below)
    from http.client import HTTPSConnection

    conn = HTTPSConnection(endpoint.replace("https://", ""))
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
    }
    conn.request("POST", "/moderate", json=payload, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return normalize_response(eval(data))  # Convert response to dict
