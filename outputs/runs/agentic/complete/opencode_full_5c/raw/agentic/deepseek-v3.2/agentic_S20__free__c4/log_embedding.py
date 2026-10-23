import os
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import cohere

from observability_models import LogEvent


def embed_log_message_sbert(log_text: str) -> Dict[str, Any]:
    """
    Embed selected log messages for semantic retrieval using Sentence Transformers.

    Args:
        log_text: The log message text to embed

    Returns:
        Dictionary with embedding results
    """
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")

        embedding = model.encode(log_text)

        return {
            "success": True,
            "log_text": log_text,
            "embedding": embedding.tolist(),
            "embedding_dimension": len(embedding),
            "model": "all-MiniLM-L6-v2",
            "provider": "Sentence Transformers (Hugging Face)",
        }

    except Exception as e:
        print(f"Error embedding with Sentence Transformers: {e}")
        return {
            "success": False,
            "error": str(e),
            "log_text": log_text,
            "provider": "Sentence Transformers",
        }


def embed_log_message_cohere(log_text: str) -> Dict[str, Any]:
    """
    Embed log messages using Cohere's embedding API.

    Args:
        log_text: The log message text to embed

    Returns:
        Dictionary with embedding results
    """
    try:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "COHERE_API_KEY environment variable not set",
                "log_text": log_text,
                "provider": "Cohere",
            }

        co = cohere.Client(api_key)

        response = co.embed(
            texts=[log_text], model="embed-english-v3.0", input_type="search_document"
        )

        embedding = response.embeddings[0]

        return {
            "success": True,
            "log_text": log_text,
            "embedding": embedding,
            "embedding_dimension": len(embedding),
            "model": "embed-english-v3.0",
            "provider": "Cohere API",
        }

    except Exception as e:
        print(f"Error embedding with Cohere: {e}")
        return {
            "success": False,
            "error": str(e),
            "log_text": log_text,
            "provider": "Cohere",
        }


def embed_logs(log_events: List[LogEvent], provider: str = "sbert") -> Dict[str, Any]:
    """
    Embed multiple log messages.

    Args:
        log_events: List of LogEvent objects
        provider: Embedding provider ('sbert' or 'cohere')

    Returns:
        Dictionary with embedding results for all logs
    """
    embeddings = []
    successful = 0
    failed = 0

    for i, log_event in enumerate(log_events):
        print(f"Embedding log {i + 1}/{len(log_events)} with {provider}...")

        if provider == "cohere":
            result = embed_log_message_cohere(log_event.message)
        else:
            result = embed_log_message_sbert(log_event.message)

        if result.get("success", False):
            embeddings.append(
                {
                    "log_index": i,
                    "log_text": log_event.message,
                    "embedding": result["embedding"],
                    "level": log_event.level.value
                    if hasattr(log_event.level, "value")
                    else str(log_event.level),
                    "timestamp": log_event.timestamp.isoformat()
                    if log_event.timestamp
                    else None,
                    "correlation_id": log_event.correlation_id,
                    "model": result.get("model"),
                    "provider": result.get("provider"),
                }
            )
            successful += 1
        else:
            failed += 1

    return {
        "total_logs": len(log_events),
        "successful_embeddings": successful,
        "failed_embeddings": failed,
        "embeddings": embeddings,
        "provider": "Sentence Transformers" if provider == "sbert" else "Cohere API",
    }


def semantic_log_search(
    query: str, log_embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on embedded logs.

    Args:
        query: Search query text
        log_embeddings: List of embedded logs
        top_k: Number of results to return

    Returns:
        List of similar logs with similarity scores
    """
    if not log_embeddings:
        return []

    try:
        provider = log_embeddings[0].get("provider", "Sentence Transformers")

        if "cohere" in provider.lower():
            query_result = embed_log_message_cohere(query)
        else:
            query_result = embed_log_message_sbert(query)

        if not query_result.get("success", False):
            print(f"Failed to embed query: {query_result.get('error')}")
            return []

        query_embedding = np.array(query_result["embedding"])

        similarities = []
        for log in log_embeddings:
            if "embedding" not in log:
                continue

            log_embedding = np.array(log["embedding"])

            similarity = np.dot(query_embedding, log_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(log_embedding)
            )

            similarities.append(
                {
                    "similarity": float(similarity),
                    "log_text": log["log_text"],
                    "level": log["level"],
                    "timestamp": log["timestamp"],
                    "correlation_id": log["correlation_id"],
                    "log_index": log["log_index"],
                }
            )

        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        return similarities[:top_k]

    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []


def cluster_logs_by_semantics(
    log_embeddings: List[Dict[str, Any]], n_clusters: int = 5
) -> Dict[str, Any]:
    """
    Cluster logs by semantic similarity.

    Args:
        log_embeddings: List of embedded logs
        n_clusters: Number of clusters to create

    Returns:
        Dictionary with clustering results
    """
    try:
        from sklearn.cluster import KMeans

        embeddings = []
        valid_indices = []

        for i, log in enumerate(log_embeddings):
            if "embedding" in log:
                embeddings.append(log["embedding"])
                valid_indices.append(i)

        if len(embeddings) < n_clusters:
            n_clusters = len(embeddings)

        if not embeddings:
            return {
                "success": False,
                "error": "No valid embeddings found",
                "clusters": [],
            }

        embeddings_array = np.array(embeddings)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings_array)

        clusters = {}
        for idx, cluster_id in enumerate(cluster_labels):
            log_idx = valid_indices[idx]
            log_data = log_embeddings[log_idx]

            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    "size": 0,
                    "logs": [],
                    "centroid": kmeans.cluster_centers_[cluster_id].tolist(),
                    "levels": set(),
                }

            clusters[cluster_id]["size"] += 1
            clusters[cluster_id]["logs"].append(
                {
                    "log_text": log_data["log_text"][:100] + "..."
                    if len(log_data["log_text"]) > 100
                    else log_data["log_text"],
                    "level": log_data["level"],
                    "similarity_to_centroid": float(
                        np.dot(
                            np.array(log_data["embedding"]),
                            kmeans.cluster_centers_[cluster_id],
                        )
                        / (
                            np.linalg.norm(np.array(log_data["embedding"]))
                            * np.linalg.norm(kmeans.cluster_centers_[cluster_id])
                        )
                    ),
                }
            )
            clusters[cluster_id]["levels"].add(log_data["level"])

        for cluster_id in clusters:
            clusters[cluster_id]["levels"] = list(clusters[cluster_id]["levels"])

        return {
            "success": True,
            "total_logs": len(log_embeddings),
            "clustered_logs": len(embeddings),
            "n_clusters": n_clusters,
            "clusters": clusters,
            "algorithm": "KMeans (scikit-learn)",
        }

    except Exception as e:
        print(f"Error clustering logs: {e}")
        return {"success": False, "error": str(e), "clusters": []}


def find_similar_incidents(
    current_logs: List[LogEvent],
    historical_embeddings: List[Dict[str, Any]],
    similarity_threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    """
    Find historically similar incidents using semantic embeddings.

    Args:
        current_logs: Current incident logs
        historical_embeddings: Historical embedded logs
        similarity_threshold: Minimum similarity score

    Returns:
        List of similar historical incidents
    """
    if not current_logs or not historical_embeddings:
        return []

    current_embeddings_result = embed_logs(current_logs, provider="sbert")
    if not current_embeddings_result.get("embeddings"):
        return []

    current_embeddings = current_embeddings_result["embeddings"]

    current_centroid = np.mean(
        [np.array(log["embedding"]) for log in current_embeddings], axis=0
    )

    historical_clusters = cluster_logs_by_semantics(
        historical_embeddings, n_clusters=10
    )

    similar_incidents = []

    if historical_clusters.get("success", False):
        for cluster_id, cluster_data in historical_clusters.get("clusters", {}).items():
            cluster_centroid = np.array(cluster_data.get("centroid", []))

            if len(cluster_centroid) == len(current_centroid):
                similarity = np.dot(current_centroid, cluster_centroid) / (
                    np.linalg.norm(current_centroid) * np.linalg.norm(cluster_centroid)
                )

                if similarity >= similarity_threshold:
                    similar_incidents.append(
                        {
                            "cluster_id": cluster_id,
                            "similarity": float(similarity),
                            "cluster_size": cluster_data["size"],
                            "levels": cluster_data["levels"],
                            "sample_logs": cluster_data["logs"][:3],
                        }
                    )

    similar_incidents.sort(key=lambda x: x["similarity"], reverse=True)

    return similar_incidents
