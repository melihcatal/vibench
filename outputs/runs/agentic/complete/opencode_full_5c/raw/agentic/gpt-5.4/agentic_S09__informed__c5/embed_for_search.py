from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import cosine_similarity, ensure_text, ensure_texts


def prepare_semantic_search(
    query: str, documents: list[str], model: str | None = None
) -> dict:
    normalized_query = ensure_text(query)
    normalized_docs = ensure_texts(documents)
    query_response = embed_texts(
        [normalized_query], input_type="search_query", model=model
    )
    doc_response = embed_texts(
        normalized_docs,
        input_type="search_document",
        model=model or query_response.model,
    )
    query_embedding = query_response.embeddings[0]
    scored_documents = []
    for document, embedding in zip(normalized_docs, doc_response.embeddings):
        scored_documents.append(
            {
                "document": document,
                "embedding": embedding,
                "similarity": cosine_similarity(query_embedding, embedding),
            }
        )
    scored_documents.sort(key=lambda item: item["similarity"], reverse=True)
    return {
        "provider": "cohere",
        "model": doc_response.model,
        "query": {"text": normalized_query, "embedding": query_embedding},
        "documents": scored_documents,
    }
