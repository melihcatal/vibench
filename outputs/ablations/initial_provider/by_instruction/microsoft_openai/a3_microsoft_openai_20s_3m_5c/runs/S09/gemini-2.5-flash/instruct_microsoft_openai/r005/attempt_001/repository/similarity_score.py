import numpy as np
from scipy.spatial.distance import cosine
from typing import List

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, normalize_text

def compute_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity score.
    """
    return 1 - cosine(embedding1, embedding2)

def similarity_score(text1: str, text2: str, model: str = "text-embedding-ada-002") -> float:
    """Embeds two texts using OpenAI and computes their cosine similarity.

    Args:
        text1: The first text string.
        text2: The second text string.
        model: The OpenAI embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        The cosine similarity score between the embeddings of the two texts.
    """
    client = EmbeddingsClient()

    normalized_text1 = normalize_text(text1)
    request1 = EmbeddingRequest(text=normalized_text1, model=model)
    embedding1_response = client.get_embedding(request1)

    normalized_text2 = normalize_text(text2)
    request2 = EmbeddingRequest(text=normalized_text2, model=model)
    embedding2_response = client.get_embedding(request2)

    return compute_cosine_similarity(embedding1_response.embedding, embedding2_response.embedding)
