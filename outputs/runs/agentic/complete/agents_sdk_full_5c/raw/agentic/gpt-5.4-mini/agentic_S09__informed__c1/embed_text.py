from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingRequest, ensure_texts


def embed_text(text: str, model: str | None = None) -> list[float]:
    texts = ensure_texts([text])
    request = EmbeddingRequest(input_texts=texts, model=get_embedding_model(model))
    client = get_openai_client()
    response = client.embeddings.create(model=request.model, input=request.input_texts[0])
    return list(response.data[0].embedding)
