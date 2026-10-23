# moderate_batch.py
"""Moderates a batch of user messages and returns per-message decisions (Azure AI Content Safety)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import List, Dict, Any

# Azure AI Content Safety batch endpoint supports up to 100 items per request
BATCH_SIZE = 100


def moderate_batch(messages: List[str], categories: list[str]) -> List[Dict[str, Any]]:
    """Iterate over a batch of messages, call moderation for each, and collect results."""
    results = []
    for i in range(0, len(messages), BATCH_SIZE):
        batch_slice = messages[i : i + BATCH_SIZE]
        batch_payload = [build_api_request(m, categories) for m in batch_slice]
        # Azure batch endpoint expects a JSON array of requests
        from http.client import HTTPSConnection

        conn = HTTPSConnection(AZURE_CONTENT_SAFETY_ENDPOINT.replace("https://", ""))
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        }
        conn.request("POST", "/moderate/batch", json=batch_payload, headers=headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        # Normalize each item in the batch response
        for item in eval(data):
            results.append(normalize_response(item))
    return results
