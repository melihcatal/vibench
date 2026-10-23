from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient, DEFAULT_EMBED_MODEL
from embeddings_models import l2_normalize


def embed_search_corpus(
    query: str, documents: list[str], model: str = DEFAULT_EMBED_MODEL
) -> dict[str, list[list[float]] | list[float]]:
    client = CohereEmbeddingsClient()
    query_response = client.embed([query], model=model, input_type="search_query")
    docs_response = client.embed(documents, model=model, input_type="search_document")
    query_vector = (
        l2_normalize(query_response.vectors[0].embedding)
        if query_response.vectors
        else []
    )
    document_vectors = [l2_normalize(item.embedding) for item in docs_response.vectors]
    return {"query_embedding": query_vector, "document_embeddings": document_vectors}
