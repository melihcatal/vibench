import asyncio
import os
import requests
from typing import AsyncGenerator

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


async def check_live_caption_safety(
    caption_stream: AsyncGenerator[str, None], threshold: float = 0.5
) -> AsyncGenerator[str, None]:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    async for caption in caption_stream:
        if not caption.strip():
            continue
        payload = {
            "comment": {"text": caption},
            "requestedAttributes": {"TOXICITY": {}},
        }
        resp = await asyncio.to_thread(requests.post, url, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            score = (
                data.get("attributeScores", {})
                .get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )
            if score < threshold:
                yield caption
        else:
            yield caption
