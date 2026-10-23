from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import create_embedding_request, fetch_embeddings
from embeddings_models import SearchEmbeddingBundle, l2_normalize


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_for_search(
    query: str,
    documents: Sequence[str],
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int | None = None,
    normalize: bool = True,
) -> SearchEmbeddingBundle:
    document_request = create_embedding_request(documents, model=model, dimensions=dimensions)
    query_request = create_embedding_request([query], model=model, dimensions=dimensions)

    query_response = fetch_embeddings(query_request)
    document_response = fetch_embeddings(document_request)

    query_vector = query_response.vectors[0].embedding
    document_vectors = [item.embedding for item in sorted(document_response.vectors, key=lambda item: item.index)]

    if normalize:
        query_vector = l2_normalize(query_vector)
        document_vectors = [l2_normalize(vector) for vector in document_vectors]

    return SearchEmbeddingBundle(query=query_vector, documents=document_vectors, model=model)
