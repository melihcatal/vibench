from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDINGS_MODEL, create_embeddings
from embeddings_models import cosine_similarity, normalize_text, normalize_texts


def embed_for_search(
    query: str, documents: list[str], model: str = OPENAI_EMBEDDINGS_MODEL
) -> dict:
    normalized_query = normalize_text(query)
    normalized_docs = normalize_texts(documents)
    result = create_embeddings([normalized_query, *normalized_docs], model=model)
    vectors = [item.embedding for item in result.vectors]
    query_vector = vectors[0] if vectors else []
    doc_vectors = vectors[1:] if len(vectors) > 1 else []
    ranked = sorted(
        (
            {
                "document": doc,
                "score": cosine_similarity(query_vector, vector),
                "embedding": vector,
            }
            for doc, vector in zip(normalized_docs, doc_vectors, strict=False)
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    return {
        "provider": "OpenAI",
        "model": result.model,
        "query": normalized_query,
        "query_embedding": query_vector,
        "results": ranked,
        "usage": result.usage,
    }
