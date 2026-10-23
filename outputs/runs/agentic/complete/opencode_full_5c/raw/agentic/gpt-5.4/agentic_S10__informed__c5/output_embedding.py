from __future__ import annotations

import os
from typing import List

import cohere

from model_models import EmbeddingRequest


COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def embed_output(
    request: EmbeddingRequest, model: str = COHERE_EMBED_MODEL
) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY is required")
    client = cohere.ClientV2(api_key=api_key)
    response = client.embed(
        model=model,
        input_type=request.input_type,
        embedding_types=["float"],
        texts=[request.text],
    )
    return response.embeddings.float[0]
