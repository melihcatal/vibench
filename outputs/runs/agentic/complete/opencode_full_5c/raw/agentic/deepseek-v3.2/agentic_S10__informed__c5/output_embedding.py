import os
import numpy as np
from openai import OpenAI


def embed_text(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Embed model outputs using OpenAI embeddings API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(model=model, input=text)

    embedding = response.data[0].embedding
    return np.array(embedding)


def embed_texts(texts: list, model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Embed multiple texts using OpenAI embeddings API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(model=model, input=texts)

    embeddings = [data.embedding for data in response.data]
    return np.array(embeddings)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
