import os
import requests
from typing import AsyncIterable

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def check_unsafe_content(text: str) -> dict:
    """Checks text for unsafe content using Perspective API."""
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    response.raise_for_status()
    return response.json()


async def live_caption_safety(captions: AsyncIterable[str]):
    """Checks live transcript text for unsafe content."""
    async for caption in captions:
        result = await check_unsafe_content(caption)
        yield {
            "text": caption,
            "safety_scores": result.get("attributeScores", {}),
        }
