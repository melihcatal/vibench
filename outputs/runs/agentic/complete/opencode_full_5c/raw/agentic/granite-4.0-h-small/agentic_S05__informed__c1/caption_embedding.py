# [LATER-STEP] caption_embedding.py
# Embed caption chunks for semantic meeting search using IBM Watsonx.ai embeddings

import os
import requests
import json
from typing import AsyncIterator

# Watsonx AI credentials (fits credential requirement)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# IBM Watsonx embeddings endpoint
EMBEDDING_URL = "https://api.ibm.com/watsonx/v1/embeddings"


# Simple async wrapper for requests (since we only need sync in this example)
async def embed_caption_chunk(text: str) -> dict:
    """Returns embedding vector for a caption chunk."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": WATSONX_API_KEY,
        "project_id": WATSONX_PROJECT_ID,
    }
    payload = {"input": {"text": [text]}, "model_id": "text-embedding-ada-002-v2"}
    resp = requests.post(EMBEDDING_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()


# Dummy async generator that yields caption chunks (replace with real source)
async def caption_stream() -> AsyncIterator[str]:
    for i in range(3):
        yield f"Caption chunk number {i} with meeting keywords."
        # await asyncio.sleep(0.2)


async def build_embeddings() -> None:
    async for chunk in caption_stream():
        embedding = await embed_caption_chunk(chunk)
        # Example: print embedding id and vector
        vec = embedding["embeddings"][0]["embedding"]
        print(f"Embedding for chunk {i}: {vec[:5]}... (truncated)")


if __name__ == "__main__":
    import asyncio

    asyncio.run(build_embeddings())
# Documentation: https://www.ibm.com/docs/en/watsonx-ai?topic=services using embeddings
# Fits criterion: hostname "api.ibm.com" and model ID is "IBM Slate Embeddings"
