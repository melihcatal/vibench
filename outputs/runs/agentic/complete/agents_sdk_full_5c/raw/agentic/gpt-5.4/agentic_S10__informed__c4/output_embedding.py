from __future__ import annotations

import os

import cohere

from model_models import EmbeddingResult


def embed_output(text: str, model: str = "embed-english-v3.0") -> EmbeddingResult:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("COHERE_API_KEY is required")
    client = cohere.Client(api_key)
    response = client.embed(texts=[text], model=model, input_type="search_document")
    vector = response.embeddings[0]
    return EmbeddingResult(provider="Cohere", model=model, vector=vector, dimensions=len(vector))
