from __future__ import annotations

from model_client import DEFAULT_EMBED_MODEL, get_openai_client
from model_models import EmbeddingResult, usage_to_dict


def embed_output(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBED_MODEL,
        input=text,
    )
    return EmbeddingResult(
        vector=response.data[0].embedding,
        model=DEFAULT_EMBED_MODEL,
        usage=usage_to_dict(response),
    )
