from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def embed_for_search(query: str, documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    payload = [query, *documents]
    result = create_embeddings(payload, model=model)
    query_vector = result.vectors[0]
    document_vectors = result.vectors[1:]
    ranked = []
    for index, (document, vector) in enumerate(zip(documents, document_vectors)):
        ranked.append(
            {
                "index": index,
                "document": document,
                "score": cosine_similarity(query_vector, vector),
                "embedding": vector,
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {
        "provider": "openai",
        "model": result.model,
        "query_embedding": query_vector,
        "results": ranked,
        "usage": result.usage,
    }
