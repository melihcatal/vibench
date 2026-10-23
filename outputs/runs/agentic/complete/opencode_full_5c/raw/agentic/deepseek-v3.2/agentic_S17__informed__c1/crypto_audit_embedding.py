import os
import json
from typing import Dict, Any, List, Optional
import openai


class CryptoAuditEmbedder:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "text-embedding-3-small"

    def embed_audit_note(self, audit_note: str) -> List[float]:
        """
        Embed a crypto audit note for semantic search.

        Args:
            audit_note: Audit note text to embed

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=self.model, input=audit_note, encoding_format="float"
            )

            return response.data[0].embedding

        except Exception as e:
            raise RuntimeError(f"Failed to create embedding: {str(e)}") from e

    def embed_audit_notes_batch(self, audit_notes: List[str]) -> List[List[float]]:
        """
        Embed multiple audit notes in batch.

        Args:
            audit_notes: List of audit note texts

        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                model=self.model, input=audit_notes, encoding_format="float"
            )

            return [data.embedding for data in response.data]

        except Exception as e:
            raise RuntimeError(f"Failed to create batch embeddings: {str(e)}") from e

    def embed_crypto_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Embed a cryptographic event for semantic search.

        Args:
            event: Cryptographic event data

        Returns:
            Event with embedding
        """
        event_text = self._format_event_for_embedding(event)
        embedding = self.embed_audit_note(event_text)

        return {"event": event, "embedding": embedding, "text": event_text}

    def search_similar_events(
        self, query: str, event_embeddings: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar crypto events using semantic search.

        Args:
            query: Search query text
            event_embeddings: List of events with embeddings
            top_k: Number of results to return

        Returns:
            List of similar events with similarity scores
        """
        from numpy import dot
        from numpy.linalg import norm

        query_embedding = self.embed_audit_note(query)

        results = []
        for event_data in event_embeddings:
            event_embedding = event_data.get("embedding")
            if event_embedding:
                similarity = self._cosine_similarity(query_embedding, event_embedding)
                results.append(
                    {
                        "event": event_data.get("event"),
                        "similarity": similarity,
                        "text": event_data.get("text"),
                    }
                )

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def cluster_audit_notes(
        self, audit_notes: List[str], n_clusters: int = 3
    ) -> Dict[str, Any]:
        """
        Cluster audit notes by semantic similarity.

        Args:
            audit_notes: List of audit notes
            n_clusters: Number of clusters to create

        Returns:
            Clustering results
        """
        from sklearn.cluster import KMeans
        import numpy as np

        embeddings = self.embed_audit_notes_batch(audit_notes)
        embeddings_array = np.array(embeddings)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings_array)

        clusters = {}
        for i, (note, label) in enumerate(zip(audit_notes, cluster_labels)):
            if label not in clusters:
                clusters[label] = {
                    "notes": [],
                    "centroid": kmeans.cluster_centers_[label].tolist(),
                    "size": 0,
                }
            clusters[label]["notes"].append(
                {
                    "text": note,
                    "index": i,
                    "distance_to_centroid": float(
                        np.linalg.norm(
                            embeddings_array[i] - kmeans.cluster_centers_[label]
                        )
                    ),
                }
            )
            clusters[label]["size"] += 1

        for cluster_id in clusters:
            clusters[cluster_id]["notes"].sort(key=lambda x: x["distance_to_centroid"])

        return {
            "clusters": clusters,
            "total_notes": len(audit_notes),
            "cluster_labels": cluster_labels.tolist(),
        }

    def create_audit_index(self, audit_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a searchable index of audit events.

        Args:
            audit_events: List of audit events

        Returns:
            Search index with embeddings
        """
        embedded_events = []
        for event in audit_events:
            embedded_event = self.embed_crypto_event(event)
            embedded_events.append(embedded_event)

        return {
            "events": embedded_events,
            "total_events": len(embedded_events),
            "model": self.model,
            "index_type": "semantic",
        }

    def _format_event_for_embedding(self, event: Dict[str, Any]) -> str:
        """Format event for embedding generation."""
        parts = []

        if "operation" in event:
            parts.append(f"Operation: {event['operation']}")

        if "key_id" in event:
            parts.append(f"Key: {event['key_id']}")

        if "timestamp" in event:
            parts.append(f"Time: {event['timestamp']}")

        if "user" in event:
            parts.append(f"User: {event['user']}")

        if "result" in event:
            result = event["result"]
            if isinstance(result, dict):
                if "status" in result:
                    parts.append(f"Status: {result['status']}")
                if "error" in result:
                    parts.append(f"Error: {result['error']}")
            else:
                parts.append(f"Result: {result}")

        if "notes" in event:
            parts.append(f"Notes: {event['notes']}")

        return ". ".join(parts)

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        from numpy import dot
        from numpy.linalg import norm
        import numpy as np

        v1 = np.array(vec1)
        v2 = np.array(vec2)

        if norm(v1) == 0 or norm(v2) == 0:
            return 0.0

        return float(dot(v1, v2) / (norm(v1) * norm(v2)))


def embed_crypto_audit(audit_text: str) -> List[float]:
    """
    Convenience function to embed crypto audit text.

    Args:
        audit_text: Audit text to embed

    Returns:
        Embedding vector
    """
    embedder = CryptoAuditEmbedder()
    return embedder.embed_audit_note(audit_text)
