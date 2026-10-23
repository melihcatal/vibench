import os
from typing import List

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class BatchTextEmbedder:
    """Generate embeddings for a batch of texts using IBM Slate Embeddings."""

    def __init__(self):
        self.client = EmbeddingsClient()
        self.model = self.client.get_embeddings_model()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        request = EmbeddingRequest(texts=texts)
        response = self.model.generate_embeddings(**request.to_dict())
        embedding_response = EmbeddingResponse(
            data=response["results"], model_id=self.model.model_id
        )
        return embedding_response.get_normalized_embeddings()


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts."""
    if not texts:
        raise ValueError("Texts list must not be empty.")
    return BatchTextEmbedder().embed_batch(texts)
