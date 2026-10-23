import os
from typing import List, Optional
import numpy as np


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Embed narration scripts for voice-asset search using OpenAI Embeddings."""
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=text)

    return response.data[0].embedding


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Embed multiple narration scripts in batch using OpenAI Embeddings."""
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in response.data]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two embedding vectors."""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)

    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def find_similar_voices(
    query_embedding: List[float], voice_embeddings: List[List[float]], top_k: int = 5
) -> List[int]:
    """Find most similar voice assets based on script embeddings."""
    similarities = []
    for i, voice_embedding in enumerate(voice_embeddings):
        similarity = cosine_similarity(query_embedding, voice_embedding)
        similarities.append((i, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return [idx for idx, _ in similarities[:top_k]]
