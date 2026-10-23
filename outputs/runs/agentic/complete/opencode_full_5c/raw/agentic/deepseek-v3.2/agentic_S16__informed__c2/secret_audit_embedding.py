import os
import openai
from typing import List, Dict, Any, Optional
import numpy as np


def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    """
    Embed secret audit notes for semantic search using OpenAI embeddings.

    Args:
        audit_notes: Audit notes text to embed

    Returns:
        Embedding vector as list of floats
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=audit_notes, encoding_format="float"
        )

        embedding = response.data[0].embedding
        return embedding

    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}") from e


def embed_multiple_audit_notes(audit_notes_list: List[str]) -> List[List[float]]:
    """
    Embed multiple secret audit notes for batch processing.

    Args:
        audit_notes_list: List of audit notes texts

    Returns:
        List of embedding vectors
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=audit_notes_list,
            encoding_format="float",
        )

        embeddings = [item.embedding for item in response.data]
        return embeddings

    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error generating batch embeddings: {e}") from e


def search_similar_audits(
    query: str, audit_embeddings: Dict[str, List[float]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar audit notes using cosine similarity.

    Args:
        query: Search query text
        audit_embeddings: Dictionary mapping audit IDs to embeddings
        top_k: Number of top results to return

    Returns:
        List of similar audits with similarity scores
    """
    # Embed the query
    query_embedding = embed_secret_audit_notes(query)

    # Calculate cosine similarities
    similarities = []

    for audit_id, embedding in audit_embeddings.items():
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append(
            {"audit_id": audit_id, "similarity": similarity, "embedding": embedding}
        )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Return top-k results
    return similarities[:top_k]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same dimension")

    # Convert to numpy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    # Calculate dot product and norms
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(similarity)


def cluster_audit_notes(
    audit_embeddings: Dict[str, List[float]], n_clusters: int = 3
) -> Dict[str, Any]:
    """
    Cluster audit notes using K-means on embeddings.

    Args:
        audit_embeddings: Dictionary mapping audit IDs to embeddings
        n_clusters: Number of clusters to create

    Returns:
        Clustering results
    """
    if len(audit_embeddings) < n_clusters:
        raise ValueError(f"Need at least {n_clusters} audits for clustering")

    try:
        from sklearn.cluster import KMeans

        # Prepare data
        audit_ids = list(audit_embeddings.keys())
        embeddings = np.array([audit_embeddings[audit_id] for audit_id in audit_ids])

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)

        # Calculate cluster centers
        cluster_centers = kmeans.cluster_centers_.tolist()

        # Organize results by cluster
        clusters = {}
        for i in range(n_clusters):
            cluster_audit_ids = [
                audit_ids[j] for j in range(len(audit_ids)) if cluster_labels[j] == i
            ]
            clusters[f"cluster_{i}"] = {
                "audit_ids": cluster_audit_ids,
                "size": len(cluster_audit_ids),
                "center": cluster_centers[i],
            }

        # Calculate silhouette score if possible
        from sklearn.metrics import silhouette_score

        if len(set(cluster_labels)) > 1:
            silhouette_avg = silhouette_score(embeddings, cluster_labels)
        else:
            silhouette_avg = 0.0

        return {
            "n_clusters": n_clusters,
            "total_audits": len(audit_ids),
            "clusters": clusters,
            "cluster_labels": cluster_labels.tolist(),
            "silhouette_score": silhouette_avg,
            "inertia": float(kmeans.inertia_),
        }

    except ImportError:
        raise ImportError(
            "scikit-learn is required for clustering. Install with: pip install scikit-learn"
        )
    except Exception as e:
        raise RuntimeError(f"Error clustering audit notes: {e}") from e


def analyze_audit_patterns(audit_notes_list: List[str]) -> Dict[str, Any]:
    """
    Analyze patterns in audit notes using embeddings.

    Args:
        audit_notes_list: List of audit notes

    Returns:
        Pattern analysis results
    """
    # Generate embeddings for all audit notes
    embeddings = embed_multiple_audit_notes(audit_notes_list)

    # Calculate pairwise similarities
    n_audits = len(audit_notes_list)
    similarity_matrix = np.zeros((n_audits, n_audits))

    for i in range(n_audits):
        for j in range(i, n_audits):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity

    # Calculate average similarity
    avg_similarity = np.mean(similarity_matrix)

    # Find most similar pair
    max_similarity = -1
    most_similar_pair = None

    for i in range(n_audits):
        for j in range(i + 1, n_audits):
            if similarity_matrix[i][j] > max_similarity:
                max_similarity = similarity_matrix[i][j]
                most_similar_pair = (i, j)

    # Find outlier (least similar to others)
    avg_similarities = np.mean(similarity_matrix, axis=1)
    outlier_index = np.argmin(avg_similarities)

    return {
        "n_audits": n_audits,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "average_similarity": float(avg_similarity),
        "max_similarity": float(max_similarity) if most_similar_pair else 0.0,
        "most_similar_pair": most_similar_pair,
        "outlier_index": int(outlier_index),
        "outlier_similarity": float(avg_similarities[outlier_index]),
        "similarity_matrix": similarity_matrix.tolist(),
    }
