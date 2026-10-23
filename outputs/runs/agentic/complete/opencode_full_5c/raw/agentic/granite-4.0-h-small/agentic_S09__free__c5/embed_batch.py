import embeddings_client

# Direct Embeddings API integration (example provider: OpenAI)


def embed_batch(texts: list) -> list:
    """Generate embedding vectors for a batch of texts.\n    Returns a list of lists, each inner list is the embedding for one text.\n"""
    client = embeddings_client.EmbeddingsClient()
    response = client.create_embedding(model="text-embedding-ada-002", input=texts)
    # Assume response returns a list of embeddings in order matching input texts
    return [emb["embedding"] for emb in response]
