from __future__ import annotations

import os

import cohere

from model_models import EmbeddingResult


COHERE_EMBED_MODEL = "embed-english-v3.0"


def embed_platform_output(text: str) -> EmbeddingResult:
    client = cohere.Client(os.environ["COHERE_API_KEY"])
    response = client.embed(
        texts=[text],
        model=COHERE_EMBED_MODEL,
        input_type="search_document",
        embedding_types=["float"],
    )
    vector = response.embeddings.float_[0]
    return EmbeddingResult(embedding=vector, dimensions=len(vector), raw=response)
