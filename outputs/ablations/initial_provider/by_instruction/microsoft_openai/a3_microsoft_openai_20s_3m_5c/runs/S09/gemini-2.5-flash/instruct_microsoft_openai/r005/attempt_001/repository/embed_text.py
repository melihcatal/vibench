from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text

def embed_text(text: str, model: str = "text-embedding-ada-002") -> EmbeddingResponse:
    """Generates an embedding vector for a single text string using OpenAI.

    Args:
        text: The input text string.
        model: The OpenAI embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        An EmbeddingResponse containing the embedding vector and metadata.
    """
    client = EmbeddingsClient()
    normalized_text = normalize_text(text)
    request = EmbeddingRequest(text=normalized_text, model=model)
    return client.get_embedding(request)

