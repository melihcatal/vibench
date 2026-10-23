from __future__ import annotations

import os
from typing import Iterable, List

import cohere


COHERE_MODEL = "embed-multilingual-v3.0"


def translation_memory_embedding(
    segments: Iterable[str], input_type: str = "search_document"
) -> List[List[float]]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        model=COHERE_MODEL,
        texts=[str(segment) for segment in segments],
        input_type=input_type,
        embedding_types=["float"],
    )
    return response.embeddings.float
