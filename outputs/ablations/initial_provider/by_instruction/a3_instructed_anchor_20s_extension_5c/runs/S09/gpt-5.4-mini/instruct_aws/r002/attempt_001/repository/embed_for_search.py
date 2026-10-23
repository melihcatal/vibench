from embed_text import embed_text


def embed_for_search(query: str, documents: list[str]) -> dict[str, list[list[float]] | list[float]]:
    query_embedding = embed_text(query).embedding
    document_embeddings = [embed_text(document).embedding for document in documents]
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
