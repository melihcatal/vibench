from __future__ import annotations

import os
from typing import Iterable, List

import httpx


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"


async def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    inputs = [chunk for chunk in chunks if chunk.strip()]
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {"model": "text-embedding-3-small", "input": inputs}
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OPENAI_EMBEDDINGS_URL, json=payload, headers=headers
        )
        response.raise_for_status()
        body = response.json()
    return [item["embedding"] for item in body["data"]]
