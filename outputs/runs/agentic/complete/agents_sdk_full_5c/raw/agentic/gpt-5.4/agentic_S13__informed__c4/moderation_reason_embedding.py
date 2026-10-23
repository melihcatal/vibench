from __future__ import annotations

import os
from typing import Iterable, List

import cohere


COHERE_MODEL = "embed-english-v3.0"


def moderation_reason_embedding(rationales: Iterable[str], input_type: str = "search_document") -> dict:
    client = cohere.Client(os.environ["COHERE_API_KEY"])
    texts: List[str] = list(rationales)
    response = client.embed(
        texts=texts,
        model=COHERE_MODEL,
        input_type=input_type,
        embedding_types=["float"],
    )
    return {
        "provider": "Cohere Embed API",
        "model": COHERE_MODEL,
        "embeddings": response.embeddings.float,
        "count": len(texts),
    }
