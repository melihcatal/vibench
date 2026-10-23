from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity, l2_normalize


def embed_for_search(query: str, documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> dict[str, object]:
    response = create_embeddings([query, *documents], model=model)
    ordered = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
    query_vector = l2_normalize(ordered[0])
    document_vectors = [l2_normalize(vector) for vector in ordered[1:]]
    scored_documents = [
        {
            "document": document,
            "score": cosine_similarity(query_vector, vector),
            "embedding": vector,
        }
        for document, vector in zip(documents, document_vectors)
    ]
    scored_documents.sort(key=lambda item: item["score"], reverse=True)
    return {
        "query_embedding": query_vector,
        "documents": scored_documents,
        "model": response.model,
    }
