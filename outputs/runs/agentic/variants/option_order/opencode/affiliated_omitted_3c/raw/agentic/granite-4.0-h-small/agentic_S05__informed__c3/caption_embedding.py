# caption_embedding.py
# [LATER-STEP]
# Embed caption chunks for semantic meeting search using Cohere embeddings API

import os
import asyncio
import json
import aiohttp
from typing import List, Dict

# Load Cohere API key from environment
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "${COHERE_API_KEY}")

EMBED_ENDPOINT = "https://api.cohere.com/v1/embed"
MODEL = "embed-english-light-v3.0"  # default model, can be overridden

HEADERS = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json",
}


async def embed_text(text: str, model: str = MODEL) -> List[float]:
    """Send a single text string to Cohere embedding endpoint and return vector."""
    payload = {
        "text": [text],
        "model": model,
    }
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.post(EMBED_ENDPOINT, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            # Cohere returns list of embeddings under data.embeddings
            return data["embeddings"][0]


async def embed_caption_batch(captions: List[str]) -> List[Dict[str, List[float]]]:
    """Embed a list of caption strings in parallel."""
    tasks = [embed_text(cap) for cap in captions]
    results = await asyncio.gather(*tasks)
    return [{"caption": caps, "embedding": vec} for caps, vec in zip(captions, results)]


# Example usage: embed live captions as they arrive
async def run_embedding_pipeline(recognizer):
    batch = []
    async for caption in recognizer.interim_results():
        txt = extract_transcript(caption)
        if txt:
            batch.append(txt)
            if len(batch) >= 5:
                batched = await embed_caption_batch(batch)
                for item in batched:
                    print(
                        "Embedded caption:",
                        item["caption"][:50],
                        "... ->",
                        item["embedding"][:5],
                        ".",
                    )
                batch.clear()
    # Embed any remaining captions
    if batch:
        await embed_caption_batch(batch)


# Helper to pull transcript from Deepgram result dict


def extract_transcript(result: dict) -> str:
    try:
        return result["results"][0]["alternatives"][0]["transcript"]
    except (KeyError, IndexError, TypeError):
        return ""


if __name__ == "__main__":
    # Demo with a dummy recognizer reading a local WAV file
    import sys

    audio_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )
    asyncio.run(run_embedding_pipeline(recognizer))

# Export helpers for other modules
__all__ = ["embed_text", "embed_caption_batch", "extract_transcript"]
