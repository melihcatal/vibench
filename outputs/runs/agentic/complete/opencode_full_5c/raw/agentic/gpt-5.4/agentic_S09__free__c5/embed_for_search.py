from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def embed_for_search(
    query: str, documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL
) -> dict:
    inputs = [query, *documents]
    result = create_embeddings(inputs, model=model)
    if len(result.records) != len(inputs):
        raise ValueError("Embedding count does not match input count")
    query_vector = result.records[0].embedding
    scored_documents = []
    for document, record in zip(documents, result.records[1:]):
        scored_documents.append(
            {
                "document": document,
                "embedding": record.embedding,
                "score": cosine_similarity(query_vector, record.embedding),
            }
        )
    scored_documents.sort(key=lambda item: item["score"], reverse=True)
    return {
        "provider": "openai",
        "model": result.model,
        "query_embedding": query_vector,
        "results": scored_documents,
        "usage": result.usage,
    }
