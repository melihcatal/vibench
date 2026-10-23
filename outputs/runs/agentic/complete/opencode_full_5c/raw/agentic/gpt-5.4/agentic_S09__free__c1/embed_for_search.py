from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import cosine_similarity, normalize_text, normalize_texts


def embed_for_search(query: str, documents: list[str]) -> dict[str, object]:
    client = CohereEmbeddingsClient()
    normalized_query = normalize_text(query)
    normalized_documents = normalize_texts(documents)
    query_response = client.embed([normalized_query], input_type="search_query")
    document_response = client.embed(normalized_documents, input_type="search_document")
    query_embedding = query_response.embeddings[0]
    ranked = sorted(
        [
            {
                "document": document,
                "embedding": embedding,
                "score": cosine_similarity(query_embedding, embedding),
            }
            for document, embedding in zip(
                normalized_documents, document_response.embeddings
            )
        ],
        key=lambda item: item["score"],
        reverse=True,
    )
    return {
        "provider": "cohere",
        "model": client.model,
        "query": normalized_query,
        "query_embedding": query_embedding,
        "results": ranked,
    }
