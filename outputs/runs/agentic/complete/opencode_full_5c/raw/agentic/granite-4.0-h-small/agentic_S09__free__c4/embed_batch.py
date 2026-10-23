import embeddings_client
import embeddings_models


def embed_batch(texts: list[str]) -> list[dict]:
    """Generate embedding vectors for a batch of text strings.
    Returns a list of dictionaries, each containing an embedding vector and metadata.
    """
    client = embeddings_client.get_client()
    payload = embeddings_models.EmbeddingBatchRequest(inputs=texts)
    response = client.embed_batch(payload)
    return embeddings_models.normalize_embedding_batch_response(response)
