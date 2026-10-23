from embeddings_client import EmbeddingsClient
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse, normalize_text
from typing import List

def embed_batch(texts: List[str], model: str = "text-embedding-ada-002") -> BatchEmbeddingResponse:
    """Generates embedding vectors for a batch of text strings using OpenAI.

    Args:
        texts: A list of input text strings.
        model: The OpenAI embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        A BatchEmbeddingResponse containing the embedding vectors and metadata.
    """
    client = EmbeddingsClient()
    normalized_texts = [normalize_text(text) for text in texts]
    request = BatchEmbeddingRequest(texts=normalized_texts, model=model)
    return client.get_batch_embeddings(request)

