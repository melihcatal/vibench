from __future__ import annotations

from model_client import DEFAULT_EMBEDDING_MODEL, get_openai_client
from model_models import EmbeddingResult, usage_to_dict


def embed_output(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    return EmbeddingResult(
        provider="openai",
        model=DEFAULT_EMBEDDING_MODEL,
        embedding=response.data[0].embedding,
        usage=usage_to_dict(
            total_tokens=getattr(response.usage, "total_tokens", None)
            if getattr(response, "usage", None)
            else None
        ),
    )
