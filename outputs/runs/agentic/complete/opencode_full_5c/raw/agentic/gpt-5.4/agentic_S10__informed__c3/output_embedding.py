from __future__ import annotations

import os
from typing import List

import cohere


def embed_output(text: str, input_type: str = "search_document") -> List[float]:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY is required")
    client = cohere.ClientV2(api_key=api_key)
    response = client.embed(
        model="embed-english-v3.0",
        input_type=input_type,
        texts=[text],
        embedding_types=["float"],
    )
    return list(response.embeddings.float_[0])
