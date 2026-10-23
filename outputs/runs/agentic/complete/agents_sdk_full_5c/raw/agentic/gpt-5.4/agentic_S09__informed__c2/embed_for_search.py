from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import OPENAI_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def embed_for_search(query: str, documents: Sequence[str], *, model: str = OPENAI_EMBEDDING_MODEL, dimensions: int | None = None) -> dict[str, object]:
    normalized_inputs = [query, *documents]
    response = create_embeddings(normalized_inputs, model=model, dimensions=dimensions)
    vectors = [vector.embedding for vector in sorted(response.vectors, key=lambda item: item.index)]
    query_vector = vectors[0]
    document_vectors = vectors[1:]
    ranked = sorted(
        [
            {
                "document": document,
                "embedding": embedding,
                "score": cosine_similarity(query_vector, embedding),
            }
            for document, embedding in zip(documents, document_vectors)
        ],
        key=lambda item: item["score"],
        reverse=True,
    )
    return {
        "query_embedding": query_vector,
        "documents": ranked,
        "model": model,
    }
