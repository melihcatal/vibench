from __future__ import annotations

from model_client import DEFAULT_EMBEDDING_MODEL, get_openai_client
from model_models import normalize_embedding_response


def embed_output(text: str) -> dict:
    client = get_openai_client()
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=text)
    result = normalize_embedding_response(response)
    return {"embedding": result.vector, "model": result.model, "usage": result.usage}
