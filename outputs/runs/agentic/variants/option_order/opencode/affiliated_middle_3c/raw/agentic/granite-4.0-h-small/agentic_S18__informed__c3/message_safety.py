import json
from typing import Dict, Any

# Azure Content Safety integration (REST API)
CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def is_unsafe(text: str) -> bool:
    """Check payload text for unsafe content using Azure Content Safety service."""
    import requests

    headers = {
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    response = requests.post(
        f"{CONTENT_SAFETY_ENDPOINT}/v1.0/moderation/text",
        headers=headers,
        json=payload,
        timeout=5,
    )
    response.raise_for_status()
    result = response.json()
    # Simplified check: if unsafe items exist, consider unsafe
    unsafe_items = result.get("results", [{}])[0].get("unsafeItems", [])
    return len(unsafe_items) > 0


# Usage example inside a consumer:
# if is_unsafe(event_payload["text"]):
#     handle_unsafe_case()
