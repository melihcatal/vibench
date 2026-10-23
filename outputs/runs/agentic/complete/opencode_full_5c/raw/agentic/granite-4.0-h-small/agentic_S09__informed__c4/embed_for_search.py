from embeddings_client import DirectEmbeddingsClient

# OpenAI Embeddings provider
client = DirectEmbeddingsClient(service="OpenAI")


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    """Embed query and documents for semantic search.

    Args:
        query (str): Search query.
        documents (list[str]): List of document texts.
    Returns:
        tuple[list[float], list[list[float]]]: Embedding of query and embeddings of documents.
    """
    query_emb = client.embed(text=query)
    doc_embs = client.embed_batch(texts=documents)
    return query_emb, doc_embs
