from __future__ import annotations

import os

from voyageai import Client


VOYAGE_API_KEY_ENV = "VOYAGE_API_KEY"
VOYAGE_EMBED_MODEL = "voyage-3-large"


def transcript_embedding(segments: list[dict[str, object]]) -> list[dict[str, object]]:
    if not os.getenv(VOYAGE_API_KEY_ENV):
        raise RuntimeError(
            f"Missing required environment variable: {VOYAGE_API_KEY_ENV}"
        )
    client = Client(api_key=os.getenv(VOYAGE_API_KEY_ENV))
    texts = [str(segment.get("text", "")) for segment in segments]
    response = client.embed(texts, model=VOYAGE_EMBED_MODEL, input_type="document")
    return [
        {
            **segment,
            "embedding": embedding,
            "provider": "voyageai",
            "model": VOYAGE_EMBED_MODEL,
        }
        for segment, embedding in zip(segments, response.embeddings)
    ]
