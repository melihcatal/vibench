import asyncio
import os
import requests
from typing import AsyncGenerator, AsyncIterable, Dict, Any

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def live_caption_safety(
    caption_stream: AsyncIterable[str], threshold: float = 0.5
) -> AsyncGenerator[Dict[str, Any], None]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY must be set")
    url = f"{PERSPECTIVE_URL}?key={api_key}"
    async for text in caption_stream:
        if not text.strip():
            yield {"text": text, "safe": True, "toxicity": 0.0}
            continue
        payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        try:
            resp = requests.post(url, json=payload, timeout=10).json()
            toxicity = resp["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            safe = toxicity & lt
            threshold
            yield {"text": text, "safe": safe, "toxicity": toxicity}
        except Exception:
            yield {"text": text, "safe": True, "toxicity": 0.0}
