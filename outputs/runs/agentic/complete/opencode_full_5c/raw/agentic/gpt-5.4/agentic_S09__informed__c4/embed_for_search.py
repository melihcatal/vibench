from __future__ import annotations

from embeddings_client import create_embeddings
from embeddings_models import cosine_similarity


def embed_for_search(
    query: str, documents: list[str], model: str = "embed-v4.0"
) -> dict[str, object]:
    query_response = create_embeddings([query], model=model, input_type="search_query")
    document_response = create_embeddings(
        documents, model=model, input_type="search_document"
    )
    query_embedding = query_response.results[0].embedding
    ranked = []
    for item in document_response.results:
        ranked.append(
            {
                "text": item.text,
                "embedding": item.embedding,
                "score": cosine_similarity(query_embedding, item.embedding),
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {
        "provider": "Cohere",
        "model": model,
        "query_embedding": query_embedding,
        "results": ranked,
    }
