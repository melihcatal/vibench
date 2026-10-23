import os
from typing import List

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class TextEmbedder:
    """Generate embeddings for text using IBM Slate Embeddings."""

    def __init__(self):
        self.client = EmbeddingsClient()
        self.model = self.client.get_embeddings_model()

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        request = EmbeddingRequest(texts=[text])
        response = self.model.generate_embeddings(**request.to_dict())
        embedding_response = EmbeddingResponse(
            data=response["results"], model_id=self.model.model_id
        )
        return embedding_response.get_normalized_embeddings()[0]


def embed_text(text: str) -> List[float]:
    """Generate embedding vector for one text string."""
    if not text.strip():
        raise ValueError("Text must not be empty.")
    return TextEmbedder().embed_text(text)
