import embeddings_client

# Direct Embeddings API integration (example provider: OpenAI)


def embed_for_search(query: str, documents: list) -> tuple:
    """Embed a query and a list of documents for semantic search.
    Returns a tuple (query_embedding, documents_embeddings).
    """
    client = embeddings_client.EmbeddingsClient()
    query_embedding = client.create_embedding(
        model="text-embedding-ada-002", input=query
    )["embedding"]
    doc_embeddings = client.create_embedding(
        model="text-embedding-ada-002", input=documents
    )
    # Assume response returns list of embeddings in order of documents
    doc_embeddings = [emb["embedding"] for emb in doc_embeddings]
    return query_embedding, doc_embeddings
