from __future__ import annotations

from model_client import DEFAULT_EMBED_MODEL, get_openai_client
from model_models import EmbeddingResult


def embed_output(text: str, model: str | None = None) -> EmbeddingResult:
    client = get_openai_client()
    selected_model = model or DEFAULT_EMBED_MODEL
    response = client.embeddings.create(
        model=selected_model,
        input=text,
    )
    embedding = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=selected_model,
        embedding=embedding,
        dimensions=len(embedding),
    )
