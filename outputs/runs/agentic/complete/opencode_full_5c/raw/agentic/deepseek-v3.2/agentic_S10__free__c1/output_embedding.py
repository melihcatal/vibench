import os
from typing import List, Optional
import numpy as np
from openai import OpenAI
from model_client import get_client


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI embeddings.

    Args:
        text: Text to embed
        model: Embedding model to use

    Returns:
        Embedding vector as list of floats
    """
    client = get_client()

    try:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding
        return embedding

    except Exception as e:
        raise Exception(f"Failed to embed text: {str(e)}")


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Embed multiple texts in batch.

    Args:
        texts: List of texts to embed
        model: Embedding model to use

    Returns:
        List of embedding vectors
    """
    client = get_client()

    try:
        response = client.embeddings.create(
            model=model, input=texts, encoding_format="float"
        )

        embeddings = [item.embedding for item in response.data]
        return embeddings

    except Exception as e:
        raise Exception(f"Failed to embed batch: {str(e)}")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_similar_texts(query: str, texts: List[str], top_k: int = 5) -> List[tuple]:
    """
    Find texts similar to query using embeddings.

    Args:
        query: Query text
        texts: List of texts to search
        top_k: Number of results to return

    Returns:
        List of (text, similarity_score) tuples
    """
    # Embed query and all texts
    query_embedding = embed_text(query)
    text_embeddings = embed_batch(texts)

    # Calculate similarities
    similarities = []
    for i, text_embedding in enumerate(text_embeddings):
        similarity = cosine_similarity(query_embedding, text_embedding)
        similarities.append((texts[i], similarity))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


def cluster_texts(texts: List[str], n_clusters: int = 3) -> List[int]:
    """
    Cluster texts using embeddings and K-means.

    Args:
        texts: List of texts to cluster
        n_clusters: Number of clusters

    Returns:
        Cluster labels for each text
    """
    from sklearn.cluster import KMeans

    # Get embeddings
    embeddings = embed_batch(texts)

    # Convert to numpy array
    X = np.array(embeddings)

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    return labels.tolist()


def get_embedding_model_info(model: str = "text-embedding-3-small") -> dict:
    """
    Get information about embedding models.

    Args:
        model: Embedding model identifier

    Returns:
        Dictionary with model information
    """
    model_info = {
        "text-embedding-3-small": {
            "dimensions": 1536,
            "max_tokens": 8191,
            "description": "New embedding model with lower cost",
        },
        "text-embedding-3-large": {
            "dimensions": 3072,
            "max_tokens": 8191,
            "description": "New embedding model with higher performance",
        },
        "text-embedding-ada-002": {
            "dimensions": 1536,
            "max_tokens": 8191,
            "description": "Previous generation embedding model",
        },
    }

    return model_info.get(
        model,
        {
            "dimensions": 1536,
            "max_tokens": 8191,
            "description": "Unknown embedding model",
        },
    )
