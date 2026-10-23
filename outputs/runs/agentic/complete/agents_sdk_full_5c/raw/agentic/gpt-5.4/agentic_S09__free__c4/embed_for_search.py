from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import SearchEmbeddingBundle, ensure_texts


def embed_for_search(query: str, documents: list[str], model: str = DEFAULT_EMBEDDING_MODEL) -> SearchEmbeddingBundle:
    normalized_documents = ensure_texts(documents)
    combined_inputs = [query, *normalized_documents]
    response = create_embeddings(combined_inputs, model=model)
    vectors = [item["embedding"] for item in response["data"]]
    return SearchEmbeddingBundle(
        query_vector=vectors[0],
        document_vectors=vectors[1:],
        documents=normalized_documents,
        model=model,
    )
