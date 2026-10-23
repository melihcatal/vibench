import asyncio
import os
import requests
from typing import AsyncGenerator, AsyncIterable

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

async def live_caption_safety(captions: AsyncIterable[str]) -> AsyncGenerator[str, None]:
    if not PERSPECTIVE_API_KEY:
        # Fallback if not set
        async for caption in captions:
            yield caption
        return

    async for caption in captions:
        if not caption.strip():
            yield caption
            continue
        params = {'key': PERSPECTIVE_API_KEY}
        data = {
            "comment": {"text": caption},
            "requestedAttributes": {"TOXICITY": {}}
        }
        resp = requests.post(PERSPECTIVE_URL, params=params, json=data)
        if resp.status_code == 200:
            score = resp.json().get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value', 0)
            if score > 0.7:
                yield "[UNSAFE CONTENT DETECTED]"
            else:
                yield caption
        else:
            yield caption