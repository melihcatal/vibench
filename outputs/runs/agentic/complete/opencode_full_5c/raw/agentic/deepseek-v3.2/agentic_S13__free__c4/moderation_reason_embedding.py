import os
from typing import List, Dict, Any
import openai
import numpy as np


def moderation_reason_embedding(moderation_reasons: List[str]) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval using OpenAI's embeddings API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    embeddings = []

    for reason in moderation_reasons:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=reason
        )

        embedding = response.data[0].embedding
        embeddings.append(embedding)

    embeddings_array = np.array(embeddings)

    if len(embeddings) > 1:
        centroid = np.mean(embeddings_array, axis=0)
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = cosine_similarity(embeddings[i], embeddings[j])
                similarities.append(sim)
        avg_similarity = np.mean(similarities) if similarities else 0
    else:
        centroid = embeddings_array[0] if len(embeddings) > 0 else None
        avg_similarity = 0

    return {
        "embeddings": embeddings,
        "centroid": centroid.tolist() if centroid is not None else None,
        "statistics": {
            "count": len(moderation_reasons),
            "embedding_dimension": len(embeddings[0]) if embeddings else 0,
            "average_similarity": float(avg_similarity),
            "provider": "OpenAI text-embedding-3-small",
        },
        "reasons": moderation_reasons,
    }


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)

    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_similar_cases(
    query_reason: str, case_embeddings: Dict[str, List[float]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find similar moderation cases using embedding similarity.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small", input=query_reason
    )

    query_embedding = response.data[0].embedding

    similarities = []
    for case_id, embedding in case_embeddings.items():
        sim = cosine_similarity(query_embedding, embedding)
        similarities.append(
            {"case_id": case_id, "similarity": sim, "embedding": embedding}
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]


def cluster_moderation_reasons(
    reasons: List[str], n_clusters: int = 3
) -> Dict[str, Any]:
    """
    Cluster moderation reasons using embeddings.
    """
    from sklearn.cluster import KMeans

    embeddings_result = moderation_reason_embedding(reasons)
    embeddings = embeddings_result["embeddings"]

    if len(embeddings) < n_clusters:
        n_clusters = len(embeddings)

    if n_clusters <= 0:
        return {
            "clusters": [],
            "cluster_centers": [],
            "labels": [],
            "provider": "OpenAI embeddings + scikit-learn KMeans",
        }

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    clusters = []
    for i in range(n_clusters):
        cluster_reasons = [reasons[j] for j in range(len(reasons)) if labels[j] == i]
        clusters.append(
            {
                "cluster_id": i,
                "size": len(cluster_reasons),
                "reasons": cluster_reasons,
                "center": kmeans.cluster_centers_[i].tolist(),
            }
        )

    return {
        "clusters": clusters,
        "cluster_centers": kmeans.cluster_centers_.tolist(),
        "labels": labels.tolist(),
        "provider": "OpenAI embeddings + scikit-learn KMeans",
    }
