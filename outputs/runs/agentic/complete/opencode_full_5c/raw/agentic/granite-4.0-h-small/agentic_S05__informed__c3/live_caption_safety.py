# Check live transcript text for unsafe content
# Service: Perspective API (toxicity detection)
# SDK: requests (REST)
# Authentication: PERSPECTIVE_API_KEY

import os
import requests
from typing import Dict, Any

PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

HEADERS = {"content-type": "application/json"}


async def check_unsafe_content(caption: str) -> Dict[str, Any]:
    """Return Perspective API response for a given caption.","""
    payload = {"comment": {"text": caption}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        PERSPECTIVE_ENDPOINT, headers=HEADERS, json=payload, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    # Extract toxicity score
    toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {
        "caption": caption,
        "toxicity_score": toxicity,
        "is_unsafe": toxicity > 0.8,  # arbitrary threshold
    }


# Example usage placeholder (requires async wrapper for HTTP)
# async for unsafe in check_unsafe_content_stream(caption_stream()):
#     print(unsafe)
