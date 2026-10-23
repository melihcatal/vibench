from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingRequest, EmbeddingResult, ensure_texts


def embed_batch(texts: list[str], model: str | None = None) -> list[EmbeddingResult]:
    cleaned = ensure_texts(texts)
    request = EmbeddingRequest(input_texts=cleaned, model=get_embedding_model(model))
    client = get_openai_client()
    response = client.embeddings.create(model=request.model, input=list(request.input_texts))
    results: list[EmbeddingResult] = []
    for text, item in zip(cleaned, response.data):
        results.append(EmbeddingResult(text=text, embedding=list(item.embedding)))
    return results
