import os
import json
from typing import Dict, Any
import http.client

# Use Azure AI Content Safety as the concrete text-moderation provider
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


# Minimal HTTP request helper for demonstration
def post_json(url: str, body: Dict[str, Any]) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
    }
    conn = http.client.HTTPSConnection(AZURE_CONTENT_SAFETY_ENDPOINT, timeout=10)
    conn.request("POST", url, json.dumps(body), headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    return data


def moderate_vendor_notes(text: str) -> bool:
    """
    Moderate vendor memo fields using Azure Content Safety.
    Returns True if safe, False if flagged.
    """
    payload = {"content": text, "moderation_options": {"types": ["TEXT"]}}
    result = post_json("/content_safety/v1/moderate", payload)
    if result.get("flagged"):
        return False
    return True
