from embeddings_client import embed_texts


def embed_for_search(
    query: str, documents: list[str]
) -> dict[str, list[list[float]] | list[float]]:
    query_embedding = embed_texts([query])[0]
    document_embeddings = embed_texts(documents)
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
