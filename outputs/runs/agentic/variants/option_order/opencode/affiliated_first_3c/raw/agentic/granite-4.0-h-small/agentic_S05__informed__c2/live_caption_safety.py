import os
import requests
from typing import AsyncIterable

# Perspective API credentials (environment variable)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

ASPECTS_TO_SCORE = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "THREAT"]


async def check_unsafe(captions: AsyncIterable[str]) -> AsyncIterable[bool]:
    """Yields a boolean indicating whether each caption is flagged as unsafe."""
    headers = {"key": PERSPECTIVE_API_KEY, "content-type": "application/json"}
    payload_template = {
        "comment": {"text": ""},
        "requestedAttributes": {aspect: {} for aspect in ASPECTS_TO_SCORE},
    }
    for caption in captions:
        payload = payload_template.copy()
        payload["comment"]["text"] = caption
        response = requests.post(PERSPECTIVE_ENDPOINT, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Perspective API error: {response.text}")
        scores = response.json()["attributeScores"]
        # Mark unsafe if any selected aspect crosses its threshold (default 0.5)
        is_unsafe = any(
            score["summaryScore"]["value"] >= 0.5 for score in scores.values()
        )
        yield is_unsafe


# Example usage with a streaming captions source
# async for unsafe in check_unsafe(stream_microphone_events):
#     print("Unsafe?", unsafe)
