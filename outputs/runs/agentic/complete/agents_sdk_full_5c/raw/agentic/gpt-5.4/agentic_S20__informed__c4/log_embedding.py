from __future__ import annotations

import os
from typing import Iterable, List

import cohere


EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def embed_log_messages(messages: Iterable[str]) -> List[List[float]]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=list(messages),
        model=EMBED_MODEL,
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float
