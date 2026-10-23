from __future__ import annotations

from typing import Any, Mapping

from openai import OpenAI

from storage_models import EmbeddingRequest, compact_text

client = OpenAI()
EMBEDDING_MODEL = "text-embedding-3-small"


def asset_metadata_embedding(text: str, metadata: Mapping[str, Any]) -> dict:
    request = EmbeddingRequest(text=text, metadata=metadata)
    normalized = compact_text([f"{k}: {v}" for k, v in request.metadata.items()])
    combined = compact_text([request.text, normalized])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=combined)
    vector = response.data[0].embedding
    return {"model": EMBEDDING_MODEL, "embedding": vector, "input_text": combined, "metadata": dict(request.metadata)}
