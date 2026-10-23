import os
from typing import Dict
import requests
# Using Azure AI Content Safety REST endpoint
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
    raise RuntimeError("Azure Content Safety credentials not configured")

SDK_PROVIDER = "Azure"

HEADERS = {
    "api-key": AZURE_CONTENT_SAFETY_KEY,
    "Content-type": "application/json",
    "Ocp-Apim-Trace": "true",
}


def is_safe(text: str) -> bool:
    """Check a plain text script using Azure AI Content Safety (moderation endpoint).
    Returns True if the content is marked as safe, False otherwise.
    """
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/v1.0/moderations/text"
    payload = {
        "input": {
            "kind": "plain-text",
            "text": text,
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code != 200:
        raise RuntimeError(f"Content safety request failed {response.status_code}")
    data = response.json()
    # Azure returns decisions array; we treat any decision with "+ve" == True as unsafe
    # Simplify: if any decision is flagged as unsafe, reject.
    decisions = data.get("results", [])
    for decision in decisions:
        if decision.get("decision", "allow") != "allow":
            return False
    return True

# Example usage: 
# if not is_safe(script): raise ValueError("Unsafe script")
