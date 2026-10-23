from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class TextEmbedder:
    """Generate an embedding vector for a single text string using Cohere."""

    def __init__(self):
        self.client = EmbeddingsClient().get_client()

    def embed_text(self, text: str) -> List[float]:
        request = EmbeddingRequest(texts=[text])
        response = self.client.embed(**request.to_dict())
        embedding_response = EmbeddingResponse(response)
        return embedding_response.get_normalized_embeddings()[0]


def embed_text(text: str) -> List[float]:
    return TextEmbedder().embed_text(text)