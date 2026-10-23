from embeddings_client import DEFAULT_EMBED_MODEL, embed_single_text, embed_texts
from embeddings_models import cosine_similarity, ensure_single_text, normalize_texts


def embed_search_corpus(
    query: str, documents: list[str], *, model: str = DEFAULT_EMBED_MODEL
) -> dict:
    normalized_query = ensure_single_text(query)
    normalized_documents = normalize_texts(documents)
    query_result = embed_single_text(
        normalized_query, input_type="search_query", model=model
    )
    document_results = embed_texts(
        normalized_documents, input_type="search_document", model=model
    )
    ranked = [
        {
            "text": item.text,
            "embedding": item.embedding,
            "score": cosine_similarity(query_result.embedding, item.embedding),
        }
        for item in document_results
    ]
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {
        "query": {"text": normalized_query, "embedding": query_result.embedding},
        "documents": ranked,
    }
