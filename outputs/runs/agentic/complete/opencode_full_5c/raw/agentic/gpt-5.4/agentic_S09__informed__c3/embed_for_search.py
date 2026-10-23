from __future__ import annotations

from embeddings_client import DEFAULT_EMBED_MODEL, create_embeddings
from embeddings_models import normalize_text, normalize_texts


def embed_for_search(
    query: str, documents: list[str], model: str = DEFAULT_EMBED_MODEL
) -> dict[str, list[list[float]] | list[float]]:
    normalized_query = normalize_text(query)
    normalized_documents = normalize_texts(documents)
    query_embedding = create_embeddings(
        [normalized_query], model=model, input_type="search_query"
    ).embeddings[0]
    document_embeddings = create_embeddings(
        normalized_documents, model=model, input_type="search_document"
    ).embeddings
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
