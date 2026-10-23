from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class BatchEmbedder:
    """Generate embeddings for a batch of texts using Cohere."""

    def __init__(self):
        self.client = EmbeddingsClient().get_client()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        request = EmbeddingRequest(texts=texts)
        response = self.client.embed(**request.to_dict())
        embedding_response = EmbeddingResponse(response)
        return embedding_response.get_normalized_embeddings()


def embed_batch(texts: List[str]) -> List[List[float]]:
    return BatchEmbedder().embed_batch(texts)