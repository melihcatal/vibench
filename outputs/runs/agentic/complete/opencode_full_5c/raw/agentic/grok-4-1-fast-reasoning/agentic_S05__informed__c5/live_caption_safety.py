import os
import requests
from typing import AsyncIterator
from speech_models import TranscriptChunk, TranscriptStream

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
SAFETY_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def live_caption_safety(stream: TranscriptStream) -> AsyncIterator[str]:
    async for chunk in stream:
        text = chunk["transcript"]
        if not text.strip():
            continue
        payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        resp = requests.post(
            SAFETY_URL, params={"key": PERSPECTIVE_API_KEY}, json=payload
        )
        if resp.status_code == 200:
            score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            if score < 0.5:
                yield text
