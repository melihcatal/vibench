from __future__ import annotations

import os
from typing import Iterable, List, Sequence

import cohere


DEFAULT_MODEL = "embed-english-v3.0"


def transcript_embedding(segments: Sequence[str] | Iterable[str], input_type: str = "search_document") -> dict:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY is required")
    client = cohere.Client(api_key)
    texts: List[str] = [segment for segment in segments if segment]
    response = client.embed(texts=texts, model=DEFAULT_MODEL, input_type=input_type, embedding_types=["float"])
    return {
        "provider": "Cohere",
        "model": DEFAULT_MODEL,
        "input_type": input_type,
        "embeddings": response.embeddings.float,
    }
