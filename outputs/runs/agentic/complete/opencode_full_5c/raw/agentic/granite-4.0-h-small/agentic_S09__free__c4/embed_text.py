import embeddings_client
import embeddings_models


def embed_text(text: str) -> dict:
    """Generate an embedding vector for a single text string using the Direct Embeddings API.
    Returns a dictionary containing the embedding vector and metadata.
    """
    client = embeddings_client.get_client()
    payload = embeddings_models.EmbeddingRequest(input=text)
    response = client.embed(payload)
    return embeddings_models.normalize_embedding_response(response)
