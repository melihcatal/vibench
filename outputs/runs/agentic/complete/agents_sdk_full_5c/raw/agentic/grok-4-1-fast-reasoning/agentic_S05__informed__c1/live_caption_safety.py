import asyncio
import os
import requests
from typing import AsyncGenerator

PERSPECTICE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

async def check_live_caption_safety(
    caption_chunks,
    toxicity_threshold: float = 0.5
) -> AsyncGenerator[str, None]:
    if not PERSPECTIVE_API_KEY:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}'
    async for chunk in caption_chunks:
        if not chunk.strip():
            yield chunk
            continue
        payload = {
            'comment': {'text': chunk},
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = await asyncio.to_thread(
            requests.post,
            url,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            score = data.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value', 0)
            if score > toxicity_threshold:
                continue  # skip unsafe
            else:
                yield chunk
        else:
            yield chunk
