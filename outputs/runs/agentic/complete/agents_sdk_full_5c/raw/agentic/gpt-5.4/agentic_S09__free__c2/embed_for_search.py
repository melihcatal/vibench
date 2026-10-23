from __future__ import annotations

from embeddings_client import get_embeddings_client, resolve_embedding_model
from embeddings_models import SearchEmbeddingBundle, ensure_text_list, normalize_text, parse_embedding_response


def embed_for_search(query: str, documents: list[str], model: str | None = None) -> SearchEmbeddingBundle:
    normalized_query = normalize_text(query)
    normalized_docs = ensure_text_list(documents)
    client = get_embeddings_client()
    response = client.embeddings.create(
        model=resolve_embedding_model(model),
        input=[normalized_query, *normalized_docs],
    )
    parsed = parse_embedding_response(response)
    vectors = [item.embedding for item in parsed.data]
    return SearchEmbeddingBundle(
        query_embedding=vectors[0],
        document_embeddings=vectors[1:],
    )
