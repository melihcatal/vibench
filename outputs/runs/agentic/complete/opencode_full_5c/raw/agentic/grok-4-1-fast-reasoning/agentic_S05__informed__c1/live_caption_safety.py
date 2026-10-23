import asyncio
import os
import requests
from typing import AsyncGenerator, AsyncIterable, Dict
from speech_models import TranscriptChunk


async def check_live_safety(
    transcripts: AsyncIterable[TranscriptChunk], threshold: float = 0.7
) -> AsyncGenerator[Dict[str, any], None]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    async for chunk in transcripts:
        if chunk.is_final and chunk.text.strip():
            payload = {
                "comment": {"text": chunk.text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
            }
            response = requests.post(url, json=payload)
            data = response.json()

            toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            is_unsafe = toxicity > threshold

            yield {
                "text": chunk.text,
                "is_unsafe": is_unsafe,
                "toxicity_score": toxicity,
            }
