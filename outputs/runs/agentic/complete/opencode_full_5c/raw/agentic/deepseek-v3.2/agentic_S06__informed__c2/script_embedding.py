import os
import openai
from typing import List


def get_text_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Embed narration scripts for voice-asset search using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=text)

    return response.data[0].embedding


def get_batch_embeddings(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Get embeddings for multiple texts in batch."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in response.data]


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    import numpy as np

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
