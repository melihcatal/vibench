from __future__ import annotations

from collections.abc import Sequence

from embed_batch import embed_batch
from embed_text import embed_text
from embeddings_models import DEFAULT_EMBEDDING_MODEL, cosine_similarity


def embed_for_search(
    query: str, documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL
) -> dict[str, object]:
    query_embedding = embed_text(query, model=model)
    document_embeddings = embed_batch(documents, model=model)
    ranked = sorted(
        (
            {
                "document": document,
                "embedding": embedding,
                "score": cosine_similarity(query_embedding, embedding),
            }
            for document, embedding in zip(documents, document_embeddings)
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    return {
        "query_embedding": query_embedding,
        "documents": ranked,
    }
