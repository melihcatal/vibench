from __future__ import annotations

from embeddings_client import embed_batch_request
from embeddings_models import SearchEmbeddingBundle, cosine_similarity


def embed_search_corpus(query: str, documents: list[str], model: str = "text-embedding-3-small") -> dict:
    response = embed_batch_request([query, *documents], model=model)
    ordered = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
    if not ordered:
        raise RuntimeError("OpenAI embeddings API returned no vectors.")
    bundle = SearchEmbeddingBundle(query_embedding=ordered[0], document_embeddings=ordered[1:])
    ranked = sorted(
        [
            {
                "document": document,
                "score": cosine_similarity(bundle.query_embedding, embedding),
            }
            for document, embedding in zip(documents, bundle.document_embeddings)
        ],
        key=lambda item: item["score"],
        reverse=True,
    )
    return {
        "provider": "OpenAI",
        "model": response.model,
        "query_embedding": bundle.query_embedding,
        "document_embeddings": bundle.document_embeddings,
        "ranked_results": ranked,
    }
