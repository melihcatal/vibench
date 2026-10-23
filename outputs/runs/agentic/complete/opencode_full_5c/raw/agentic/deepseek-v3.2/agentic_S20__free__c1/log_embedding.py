import json
import requests
from typing import List, Dict, Any
from observability_client import get_huggingface_client
from observability_models import EmbeddingResult


def embed_log_messages(log_messages: List[Dict[str, Any]]) -> List[EmbeddingResult]:
    """
    Embed selected log messages for semantic retrieval using Hugging Face.

    Args:
        log_messages: List of log messages with 'id' and 'message' fields

    Returns:
        List of embedding results
    """
    results = []

    try:
        hf_config = get_huggingface_client()
        api_key = hf_config["api_key"]
        api_url = hf_config["api_url"]
        model = hf_config["model"]

        # Prepare messages for embedding
        texts_to_embed = []
        message_indices = []

        for i, log in enumerate(log_messages):
            message = log.get("message", "")
            if message and len(message.strip()) > 0:
                texts_to_embed.append(message)
                message_indices.append(i)

        if not texts_to_embed:
            return []

        # Call Hugging Face API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            api_url, headers=headers, json={"inputs": texts_to_embed}
        )

        if response.status_code != 200:
            raise Exception(
                f"Hugging Face API error: {response.status_code} - {response.text}"
            )

        embeddings = response.json()

        # Map embeddings back to logs
        embedding_map = {}
        for idx, embedding in zip(message_indices, embeddings):
            embedding_map[idx] = embedding

        # Create results
        for i, log in enumerate(log_messages):
            log_id = log.get("id", f"log-{i}")
            message = log.get("message", "")

            if i in embedding_map:
                results.append(
                    EmbeddingResult(
                        log_id=log_id,
                        message=message[:500],  # Truncate for display
                        embedding=embedding_map[i],
                        model=model,
                        provider="huggingface",
                    )
                )
            else:
                # Empty embedding for empty messages
                results.append(
                    EmbeddingResult(
                        log_id=log_id,
                        message=message,
                        embedding=[],
                        model=model,
                        provider="huggingface",
                    )
                )

    except Exception as e:
        # Fallback: simple TF-IDF like embedding
        for i, log in enumerate(log_messages):
            log_id = log.get("id", f"log-{i}")
            message = log.get("message", "")

            # Create a simple hash-based embedding as fallback
            import hashlib

            hash_obj = hashlib.md5(message.encode())
            hash_bytes = hash_obj.digest()

            # Convert to list of floats
            embedding = [(byte / 255.0) for byte in hash_bytes[:16]]  # 16-dimensional

            results.append(
                EmbeddingResult(
                    log_id=log_id,
                    message=message[:500],
                    embedding=embedding,
                    model="fallback-hash",
                    provider="fallback",
                )
            )

    return results


def embed_single_log_message(log_id: str, message: str) -> EmbeddingResult:
    """
    Embed a single log message.

    Args:
        log_id: Log identifier
        message: Log message text

    Returns:
        Embedding result
    """
    results = embed_log_messages([{"id": log_id, "message": message}])
    return results[0] if results else None


def find_similar_logs(
    query_message: str, log_embeddings: List[EmbeddingResult], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find logs similar to query message using cosine similarity.

    Args:
        query_message: Query message text
        log_embeddings: List of embedded logs
        top_k: Number of similar logs to return

    Returns:
        List of similar logs with similarity scores
    """
    # Embed query message
    query_embedding_result = embed_single_log_message("query", query_message)
    if not query_embedding_result or not query_embedding_result.embedding:
        return []

    query_embedding = query_embedding_result.embedding

    # Calculate similarities
    similarities = []
    for log_embedding in log_embeddings:
        if not log_embedding.embedding:
            continue

        # Cosine similarity
        import numpy as np

        # Convert to numpy arrays
        vec1 = np.array(query_embedding)
        vec2 = np.array(log_embedding.embedding)

        # Ensure same dimensions
        min_dim = min(len(vec1), len(vec2))
        vec1 = vec1[:min_dim]
        vec2 = vec2[:min_dim]

        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (norm1 * norm2)

        similarities.append(
            {
                "log_id": log_embedding.log_id,
                "message": log_embedding.message,
                "similarity": float(similarity),
                "embedding_provider": log_embedding.provider,
            }
        )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]


def cluster_logs_by_semantics(
    log_embeddings: List[EmbeddingResult], n_clusters: int = 3
) -> Dict[str, Any]:
    """
    Cluster logs by semantic similarity.

    Args:
        log_embeddings: List of embedded logs
        n_clusters: Number of clusters to create

    Returns:
        Clustering results
    """
    if not log_embeddings or len(log_embeddings) < n_clusters:
        return {
            "clusters": [],
            "cluster_count": 0,
            "message": "Not enough logs for clustering",
        }

    try:
        import numpy as np
        from sklearn.cluster import KMeans

        # Extract embeddings
        embeddings = []
        valid_indices = []

        for i, log_embedding in enumerate(log_embeddings):
            if log_embedding.embedding:
                embeddings.append(log_embedding.embedding)
                valid_indices.append(i)

        if len(embeddings) < n_clusters:
            return {
                "clusters": [],
                "cluster_count": 0,
                "message": "Not enough valid embeddings for clustering",
            }

        # Perform K-means clustering
        embeddings_array = np.array(embeddings)
        kmeans = KMeans(
            n_clusters=min(n_clusters, len(embeddings)), random_state=42, n_init=10
        )
        cluster_labels = kmeans.fit_predict(embeddings_array)

        # Group logs by cluster
        clusters = {}
        for idx, label in zip(valid_indices, cluster_labels):
            log_embedding = log_embeddings[idx]

            if label not in clusters:
                clusters[label] = {
                    "cluster_id": int(label),
                    "logs": [],
                    "centroid": kmeans.cluster_centers_[label].tolist(),
                    "size": 0,
                }

            clusters[label]["logs"].append(
                {
                    "log_id": log_embedding.log_id,
                    "message": log_embedding.message,
                    "embedding_length": len(log_embedding.embedding),
                }
            )
            clusters[label]["size"] += 1

        # Convert to list
        cluster_list = list(clusters.values())

        # Sort clusters by size
        cluster_list.sort(key=lambda x: x["size"], reverse=True)

        return {
            "clusters": cluster_list,
            "cluster_count": len(cluster_list),
            "total_logs": len(valid_indices),
            "algorithm": "KMeans",
            "provider": log_embeddings[0].provider if log_embeddings else "unknown",
        }

    except ImportError:
        # Fallback: simple grouping by message length
        clusters = {}
        for i, log_embedding in enumerate(log_embeddings):
            if not log_embedding.embedding:
                continue

            # Simple clustering by embedding dimension
            dim = len(log_embedding.embedding)
            cluster_key = f"dim_{dim}"

            if cluster_key not in clusters:
                clusters[cluster_key] = {
                    "cluster_id": cluster_key,
                    "logs": [],
                    "size": 0,
                }

            clusters[cluster_key]["logs"].append(
                {
                    "log_id": log_embedding.log_id,
                    "message": log_embedding.message,
                    "embedding_length": dim,
                }
            )
            clusters[cluster_key]["size"] += 1

        cluster_list = list(clusters.values())
        cluster_list.sort(key=lambda x: x["size"], reverse=True)

        return {
            "clusters": cluster_list[:n_clusters],
            "cluster_count": min(len(cluster_list), n_clusters),
            "total_logs": sum(len(c["logs"]) for c in cluster_list[:n_clusters]),
            "algorithm": "dimension_based",
            "provider": "fallback",
        }
