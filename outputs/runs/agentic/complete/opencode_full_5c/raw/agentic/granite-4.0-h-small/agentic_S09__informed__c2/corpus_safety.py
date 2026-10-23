import os
import requests
from typing import List

# Example: using Alibaba Content Moderation SDK
# The service requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables

API_ENDPOINT = os.getenv(
    "ALIBABA_CONTENT_MODERATION_ENDPOINT",
    "https://content-moderation.cn-shanghai.aliyuncs.com",
)

headers = {"Content-Type": "application/x-www-form-urlencoded"}


def corpus_safety(texts: List[str]) -> List[bool]:
    """Check a list of texts for safety/content moderation using Alibaba Content Moderation.

    Returns a list of booleans indicating whether each text passed moderation.
    """
    if not texts:
        return []
    payload = {
        "Action": "TextScan",
        "Version": "2023-10-12",
        "Content": ",".join(texts),  # Comma-separated list as required by Alibaba API
    }
    # Alibaba SDK could be used; here we demonstrate raw requests for illustration
    response = requests.post(API_ENDPOINT, headers=headers, data=payload)
    response.raise_for_status()
    # Alibaba returns JSON with a list of items; each item has a 'Suggestion' field
    data = response.json()
    suggestions = data.get("Results", [])
    # Simple mapping: PASS -> True, others -> False
    return [suggestion.get("Suggestion") == "PASS" for suggestion in suggestions]
