
from typing import List

from vertexai.language_models import TextEmbeddingModel


def embed_segments(segments: List[str]) -> List[List[float]]:
    """Embeds a list of text segments using Google Cloud's Vertex AI.

    Args:
        segments: A list of text strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(segments)
    return [embedding.values for embedding in embeddings]
