import asyncio
import os
import requests
from typing import AsyncGenerator, AsyncIterator, Dict, Any


async def check_live_captions_safety(
    captions: AsyncIterator[str],
) -> AsyncGenerator[Dict[str, Any], None]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    loop = asyncio.get_event_loop()
    async for caption in captions:
        payload = {
            "comment": {"text": caption},
            "requestedAttributes": {"TOXICITY": {}},
        }
        resp = await loop.run_in_executor(None, requests.post, url, json=payload)
        data = resp.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        yield {"text": caption, "safe": score < 0.5, "toxicity_score": score}
