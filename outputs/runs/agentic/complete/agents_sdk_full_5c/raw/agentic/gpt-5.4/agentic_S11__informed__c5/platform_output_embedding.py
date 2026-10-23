from __future__ import annotations

import os

import cohere

from model_models import EmbeddingResult

DEFAULT_MODEL = "embed-english-v3.0"


def platform_output_embedding(text: str, model: str = DEFAULT_MODEL, input_type: str = "search_document") -> EmbeddingResult:
    client = cohere.Client(os.environ["COHERE_API_KEY"])
    response = client.embed(texts=[text], model=model, input_type=input_type, embedding_types=["float"])
    vector = response.embeddings.float_[0]
    return EmbeddingResult(vector=vector, model=model, dimensions=len(vector), raw=response)
