from __future__ import annotations

import os

import cohere

from model_models import EmbeddingResult

DEFAULT_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def embed_platform_output(text: str, *, model: str = DEFAULT_EMBED_MODEL) -> EmbeddingResult:
    client = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
    response = client.embed(
        model=model,
        input_type="search_document",
        embedding_types=["float"],
        texts=[text],
    )
    vector = response.embeddings.float[0]
    return EmbeddingResult(
        embedding=vector,
        model=model,
        dimensions=len(vector),
        raw={"provider": "cohere"},
    )
