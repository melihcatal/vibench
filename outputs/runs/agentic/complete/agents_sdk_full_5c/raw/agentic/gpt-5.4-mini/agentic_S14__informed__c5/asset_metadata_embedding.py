from __future__ import annotations

import os

from openai import OpenAI

from storage_models import EmbeddingRequest, EmbeddingResult, coerce_float_vector, normalize_text


OPENAI_EMBEDDING_MODEL_ENV = "OPENAI_EMBEDDING_MODEL"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_asset_metadata_and_text(text: str, metadata: dict[str, object] | None = None) -> EmbeddingResult:
    request = EmbeddingRequest(text=text, metadata=metadata or {})
    client = OpenAI()
    model = os.getenv(OPENAI_EMBEDDING_MODEL_ENV, DEFAULT_OPENAI_EMBEDDING_MODEL)
    payload = normalize_text(request.text)
    if request.metadata:
        payload = f"metadata={request.metadata}\ntext={payload}"
    response = client.embeddings.create(model=model, input=payload)
    vector = coerce_float_vector(response.data[0].embedding if response.data else [])
    return EmbeddingResult(vector=vector, raw=response)
