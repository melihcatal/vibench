import json
import numpy as np
from typing import Dict, Any, List, Optional
from sentence_transformers import SentenceTransformer
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


class LogEmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def embed_log_message(self, text: str) -> Dict[str, Any]:
        embedding = self.model.encode(text)

        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "embedding": embedding.tolist(),
            "embedding_dimension": len(embedding),
            "model": self.model_name,
            "success": True,
        }

    def embed_log_entry(self, log_entry: LogEntry) -> Dict[str, Any]:
        embedding_text = f"{log_entry.level}: {log_entry.message}"

        if log_entry.service:
            embedding_text = f"{log_entry.service} - {embedding_text}"

        embedding_result = self.embed_log_message(embedding_text)

        return {
            "log_entry": {
                "timestamp": log_entry.timestamp,
                "level": log_entry.level,
                "service": log_entry.service,
                "component": log_entry.component,
                "message_preview": log_entry.message[:100] + "..."
                if len(log_entry.message) > 100
                else log_entry.message,
            },
            "embedding": embedding_result,
            "metadata": {
                "correlation_id": log_entry.correlation_id,
                "embedding_text": embedding_text[:150] + "..."
                if len(embedding_text) > 150
                else embedding_text,
            },
        }

    def batch_embed_logs(self, log_messages: List[str]) -> List[Dict[str, Any]]:
        embeddings = self.model.encode(log_messages)

        results = []
        for i, (message, embedding) in enumerate(zip(log_messages, embeddings)):
            results.append(
                {
                    "index": i,
                    "text": message[:150] + "..." if len(message) > 150 else message,
                    "embedding": embedding.tolist(),
                    "embedding_dimension": len(embedding),
                }
            )

        return results

    def similarity_search(
        self, query: str, embeddings: List[List[float]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_embedding = self.model.encode(query)

        similarities = []
        for i, embedding in enumerate(embeddings):
            similarity = self.cosine_similarity(query_embedding, np.array(embedding))
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        return [
            {
                "rank": rank + 1,
                "index": idx,
                "similarity_score": float(score),
                "similarity_percentage": float(score * 100),
            }
            for rank, (idx, score) in enumerate(similarities[:top_k])
        ]

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def embed_recent_logs(
    minutes_ago: int = 60, limit: int = 50, service_filter: Optional[str] = None
) -> Dict[str, Any]:
    embedding_service = LogEmbeddingService()

    logs_response = fetch_recent_logs(
        minutes_ago=minutes_ago, service=service_filter, limit=limit
    )

    embedded_logs = []
    log_messages = []

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")

            if log_message:
                log_messages.append(log_message)

                embedding_result = embedding_service.embed_log_message(log_message)

                embedded_logs.append(
                    {
                        "timestamp": event.get("timestamp"),
                        "service": log_data.get("service", "unknown"),
                        "level": log_data.get("level", "INFO"),
                        "message_preview": log_message[:100] + "..."
                        if len(log_message) > 100
                        else log_message,
                        "embedding_dimension": embedding_result["embedding_dimension"],
                        "model": embedding_result["model"],
                    }
                )
        except:
            continue

    if log_messages:
        batch_embeddings = embedding_service.batch_embed_logs(log_messages)

        embedding_stats = {
            "total_embeddings": len(batch_embeddings),
            "embedding_dimension": batch_embeddings[0]["embedding_dimension"]
            if batch_embeddings
            else 0,
            "model_used": embedding_service.model_name,
        }
    else:
        batch_embeddings = []
        embedding_stats = {
            "total_embeddings": 0,
            "model_used": embedding_service.model_name,
        }

    return {
        "time_range": f"Last {minutes_ago} minutes",
        "total_logs_processed": len(logs_response.events),
        "successfully_embedded": len(embedded_logs),
        "embedding_stats": embedding_stats,
        "embedded_logs_sample": embedded_logs[:5],
        "embeddings_available": len(batch_embeddings) > 0,
    }


def search_similar_logs(
    query: str,
    minutes_ago: int = 120,
    top_k: int = 5,
    service_filter: Optional[str] = None,
) -> Dict[str, Any]:
    embedding_service = LogEmbeddingService()

    logs_response = fetch_recent_logs(
        minutes_ago=minutes_ago, service=service_filter, limit=100
    )

    log_entries = []
    log_messages = []

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")

            if log_message:
                log_entries.append(
                    {
                        "timestamp": event.get("timestamp"),
                        "service": log_data.get("service", "unknown"),
                        "level": log_data.get("level", "INFO"),
                        "message": log_message,
                        "full_data": log_data,
                    }
                )
                log_messages.append(log_message)
        except:
            continue

    if not log_messages:
        return {
            "query": query,
            "matches_found": 0,
            "time_range": f"Last {minutes_ago} minutes",
            "message": "No logs found to search",
        }

    embeddings = embedding_service.batch_embed_logs(log_messages)
    embedding_vectors = [item["embedding"] for item in embeddings]

    similarity_results = embedding_service.similarity_search(
        query, embedding_vectors, top_k
    )

    matched_logs = []
    for result in similarity_results:
        idx = result["index"]
        if idx < len(log_entries):
            log_entry = log_entries[idx]
            matched_logs.append(
                {
                    "rank": result["rank"],
                    "similarity_score": result["similarity_score"],
                    "similarity_percentage": result["similarity_percentage"],
                    "timestamp": log_entry["timestamp"],
                    "service": log_entry["service"],
                    "level": log_entry["level"],
                    "message": log_entry["message"][:150] + "..."
                    if len(log_entry["message"]) > 150
                    else log_entry["message"],
                }
            )

    return {
        "query": query,
        "matches_found": len(matched_logs),
        "time_range": f"Last {minutes_ago} minutes",
        "search_model": embedding_service.model_name,
        "top_matches": matched_logs,
        "search_stats": {
            "total_logs_searched": len(log_messages),
            "embedding_dimension": embeddings[0]["embedding_dimension"]
            if embeddings
            else 0,
        },
    }


def cluster_similar_logs(
    minutes_ago: int = 180, limit: int = 100, n_clusters: int = 5
) -> Dict[str, Any]:
    from sklearn.cluster import KMeans

    embedding_service = LogEmbeddingService()

    logs_response = fetch_recent_logs(minutes_ago=minutes_ago, limit=limit)

    log_entries = []
    log_messages = []

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")

            if log_message:
                log_entries.append(
                    {
                        "timestamp": event.get("timestamp"),
                        "service": log_data.get("service", "unknown"),
                        "level": log_data.get("level", "INFO"),
                        "message": log_message,
                    }
                )
                log_messages.append(log_message)
        except:
            continue

    if len(log_messages) < n_clusters:
        return {
            "clusters_found": 0,
            "message": f"Not enough logs for clustering. Need at least {n_clusters}, found {len(log_messages)}",
            "time_range": f"Last {minutes_ago} minutes",
        }

    embeddings = embedding_service.batch_embed_logs(log_messages)
    embedding_vectors = np.array([item["embedding"] for item in embeddings])

    kmeans = KMeans(n_clusters=min(n_clusters, len(log_messages)), random_state=42)
    cluster_labels = kmeans.fit_predict(embedding_vectors)

    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []

        clusters[label].append(
            {
                "message": log_entries[i]["message"][:100] + "..."
                if len(log_entries[i]["message"]) > 100
                else log_entries[i]["message"],
                "service": log_entries[i]["service"],
                "level": log_entries[i]["level"],
            }
        )

    cluster_summaries = []
    for cluster_id, logs in clusters.items():
        cluster_summaries.append(
            {
                "cluster_id": int(cluster_id),
                "size": len(logs),
                "sample_messages": [log["message"] for log in logs[:3]],
                "services": list(set(log["service"] for log in logs if log["service"])),
                "levels": list(set(log["level"] for log in logs)),
            }
        )

    return {
        "total_logs_clustered": len(log_messages),
        "clusters_found": len(clusters),
        "time_range": f"Last {minutes_ago} minutes",
        "clustering_model": "KMeans",
        "embedding_model": embedding_service.model_name,
        "cluster_summaries": cluster_summaries,
    }


if __name__ == "__main__":
    embedding_service = LogEmbeddingService()

    test_message = "Database connection timeout after 30 seconds"
    embedding = embedding_service.embed_log_message(test_message)
    print(f"Embedding created: {embedding['embedding_dimension']} dimensions")

    recent_embeddings = embed_recent_logs(minutes_ago=30, limit=20)
    print(f"\nRecent logs embeddings: {json.dumps(recent_embeddings, indent=2)}")

    search_results = search_similar_logs(
        query="database connection error", minutes_ago=60, top_k=3
    )
    print(f"\nSimilar logs search: {json.dumps(search_results, indent=2)}")

    clustering = cluster_similar_logs(minutes_ago=120, limit=50, n_clusters=3)
    print(f"\nLog clustering: {json.dumps(clustering, indent=2)}")
