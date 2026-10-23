from __future__ import annotations

from embeddings_client import create_embeddings
from embeddings_models import cosine_similarity



def embed_for_search(
    query: str,
    documents: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> dict[str, object]:
    if not documents:
        raise ValueError("documents must not be empty")
    response = create_embeddings([query, *documents], model=model, dimensions=dimensions)
    query_vector = response.vectors[0].embedding
    document_vectors = response.vectors[1:]
    ranked = sorted(
        [
            {
                "document": item.source_text or "",
                "score": cosine_similarity(query_vector, item.embedding),
                "embedding": item.embedding,
            }
            for item in document_vectors
        ],
        key=lambda row: row["score"],
        reverse=True,
    )
    return {
        "model": response.model,
        "query_embedding": query_vector,
        "results": ranked,
    }
