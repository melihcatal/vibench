from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import cosine_similarity


def embed_for_search(
    query: str, documents: list[str], model: str = "embed-v4.0"
) -> list[dict[str, object]]:
    client = CohereEmbeddingsClient(model=model)
    query_response = client.embed([query], input_type="search_query")
    document_response = client.embed(documents, input_type="search_document")
    query_vector = query_response.embeddings[0].values
    ranked = []
    for item in document_response.embeddings:
        ranked.append(
            {
                "document": item.text,
                "score": cosine_similarity(query_vector, item.values),
                "embedding": item.values,
            }
        )
    ranked.sort(key=lambda entry: float(entry["score"]), reverse=True)
    return ranked
