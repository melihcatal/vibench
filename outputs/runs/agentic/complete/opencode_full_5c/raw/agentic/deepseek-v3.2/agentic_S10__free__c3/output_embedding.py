import os
from typing import List, Optional
import numpy as np
from openai import OpenAI
from model_client import get_llm_client


def embed_text(text: str, model: Optional[str] = None) -> List[float]:
    """
    Embed text using OpenAI's embedding model.

    Args:
        text: Text to embed
        model: Optional embedding model to use

    Returns:
        List of embedding vectors
    """
    client = get_llm_client()

    model_to_use = model or "text-embedding-3-small"

    try:
        response = client.embeddings.create(
            model=model_to_use, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding

        return embedding

    except Exception as e:
        raise Exception(f"Failed to embed text: {str(e)}")


def embed_model_outputs(outputs: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Embed multiple model outputs for clustering or retrieval.

    Args:
        outputs: List of model output texts
        batch_size: Batch size for embedding

    Returns:
        List of embedding vectors
    """
    embeddings = []

    for i in range(0, len(outputs), batch_size):
        batch = outputs[i : i + batch_size]

        try:
            client = get_llm_client()
            response = client.embeddings.create(
                model="text-embedding-3-small", input=batch, encoding_format="float"
            )

            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)

        except Exception as e:
            # Fall back to individual embedding for failed batch
            for text in batch:
                try:
                    embedding = embed_text(text)
                    embeddings.append(embedding)
                except:
                    # Use zero vector as fallback
                    embeddings.append([0.0] * 1536)  # text-embedding-3-small dimension

    return embeddings


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

    return dot_product / (norm1 * norm2)


def find_similar_outputs(query: str, outputs: List[str], top_k: int = 5) -> List[tuple]:
    """
    Find similar model outputs to a query.

    Args:
        query: Query text
        outputs: List of model outputs to search
        top_k: Number of similar results to return

    Returns:
        List of (output_text, similarity_score) tuples
    """
    query_embedding = embed_text(query)
    output_embeddings = embed_model_outputs(outputs)

    similarities = []

    for i, output_embedding in enumerate(output_embeddings):
        similarity = cosine_similarity(query_embedding, output_embedding)
        similarities.append((outputs[i], similarity))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


def cluster_outputs(outputs: List[str], n_clusters: int = 3) -> dict:
    """
    Cluster model outputs using embeddings.

    Args:
        outputs: List of model outputs
        n_clusters: Number of clusters to create

    Returns:
        Dictionary with clustering results
    """
    from sklearn.cluster import KMeans

    embeddings = embed_model_outputs(outputs)

    if len(embeddings) < n_clusters:
        n_clusters = len(embeddings)

    if n_clusters <= 1:
        return {
            "clusters": {0: outputs},
            "centroids": [embeddings[0]] if embeddings else [],
            "model_used": "text-embedding-3-small",
            "provider": "openai",
        }

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings)

    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(outputs[i])

    return {
        "clusters": clusters,
        "centroids": kmeans.cluster_centers_.tolist(),
        "cluster_labels": cluster_labels.tolist(),
        "model_used": "text-embedding-3-small",
        "provider": "openai",
    }


def semantic_search(query: str, corpus: List[str], top_k: int = 5) -> List[dict]:
    """
    Perform semantic search on a corpus of texts.

    Args:
        query: Search query
        corpus: List of texts to search
        top_k: Number of results to return

    Returns:
        List of search results with metadata
    """
    query_embedding = embed_text(query)
    corpus_embeddings = embed_model_outputs(corpus)

    results = []

    for i, doc_embedding in enumerate(corpus_embeddings):
        similarity = cosine_similarity(query_embedding, doc_embedding)
        results.append({"text": corpus[i], "similarity": similarity, "index": i})

    # Sort by similarity (descending)
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_k]
