"""Embed secret audit notes for semantic search using OpenAI embeddings API."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI


# OpenAI API configuration for embedding generation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)


class AuditNoteEmbedder:
    """
    Embed secret audit notes using OpenAI's text-embedding-3-small model.

    Uses the OpenAI embeddings API to generate vector representations
    of audit notes for semantic search. The OpenAI API endpoint is
    api.openai.com.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_EMBEDDING_MODEL
        self.client = OpenAI(api_key=self.api_key)

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text using OpenAI.

        Args:
            text: The audit note text to embed.

        Returns:
            List of floats representing the embedding vector.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding

    def embed_audit_note(
        self,
        secret_id: str,
        operation: str,
        note_text: str,
        timestamp: Optional[datetime] = None,
        operator: Optional[str] = None,
        status: str = "completed",
    ) -> Dict[str, Any]:
        """
        Embed a complete audit note using OpenAI's text-embedding-3-small model.

        Creates a structured embedding that includes the note text
        and metadata for semantic search of audit logs.

        Args:
            secret_id: The secret that was operated on.
            operation: The operation performed (rotate, create, update, etc.)
            note_text: The audit note text to embed.
            timestamp: When the operation occurred.
            operator: Who performed the operation.
            status: The operation status.

        Returns:
            Dictionary with the embedded audit note and metadata.
        """
        timestamp = timestamp or datetime.now()
        full_text = (
            f"Secret: {secret_id}, Operation: {operation}, "
            f"Note: {note_text}, Operator: {operator or 'system'}, "
            f"Status: {status}"
        )

        embedding = self.embed_text(full_text)

        return {
            "secret_id": secret_id,
            "operation": operation,
            "note_text": note_text,
            "timestamp": timestamp.isoformat(),
            "operator": operator,
            "status": status,
            "embedding_model": self.model,
            "embedding_provider": "openai",
            "embedding": embedding,
            "embedding_dimension": len(embedding),
        }

    def embed_audit_notes_batch(
        self,
        notes: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Embed multiple audit notes using OpenAI's batch embedding API.

        Args:
            notes: List of audit note dictionaries with keys:
                   secret_id, operation, note_text, timestamp, operator, status.

        Returns:
            List of embedded audit note dictionaries.
        """
        results = []
        for note in notes:
            embedded = self.embed_audit_note(
                secret_id=note.get("secret_id", "unknown"),
                operation=note.get("operation", "unknown"),
                note_text=note.get("note_text", ""),
                timestamp=note.get("timestamp"),
                operator=note.get("operator"),
                status=note.get("status", "completed"),
            )
            results.append(embedded)
        return results

    def compute_similarity(
        self,
        embedding_a: List[float],
        embedding_b: List[float],
    ) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding_a: First embedding vector.
            embedding_b: Second embedding vector.

        Returns:
            Cosine similarity score between 0 and 1.
        """
        import math

        dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
        norm_a = math.sqrt(sum(a * a for a in embedding_a))
        norm_b = math.sqrt(sum(b * b for b in embedding_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def search_similar_notes(
        self,
        query_text: str,
        embedded_notes: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar audit notes using OpenAI embeddings.

        Embeds the query text using text-embedding-3-small and finds
        the most similar notes from a pre-embedded collection.

        Args:
            query_text: The search query text.
            embedded_notes: List of pre-embedded note dictionaries.
            top_k: Number of top results to return.

        Returns:
            List of matching notes sorted by similarity.
        """
        query_embedding = self.embed_text(query_text)

        scored_notes = []
        for note in embedded_notes:
            if "embedding" in note:
                similarity = self.compute_similarity(
                    query_embedding, note["embedding"]
                )
                scored_notes.append({
                    **note,
                    "similarity_score": similarity,
                })

        scored_notes.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_notes[:top_k]


def embed_audit_notes(
    notes: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Convenience function to embed audit notes using OpenAI embeddings.

    Args:
        notes: List of audit note dictionaries.
        api_key: Optional OpenAI API key.
        model: Optional OpenAI embedding model (default: text-embedding-3-small).

    Returns:
        List of embedded audit note dictionaries.
    """
    embedder = AuditNoteEmbedder(api_key=api_key, model=model)
    return embedder.embed_audit_notes_batch(notes)


if __name__ == "__main__":
    sample_notes = [
        {
            "secret_id": "production/api-key",
            "operation": "rotate",
            "note_text": "Rotated API key due to scheduled rotation policy",
            "timestamp": datetime.now(),
            "operator": "system",
        },
        {
            "secret_id": "production/db-credentials",
            "operation": "update",
            "note_text": "Updated database credentials after rotation",
            "timestamp": datetime.now(),
            "operator": "admin",
        },
    ]

    embedder = AuditNoteEmbedder()
    embedded = embedder.embed_audit_notes_batch(sample_notes)
    for note in embedded:
        print(
            f"Embedded: {note['secret_id']} - {note['operation']} "
            f"(dim={note['embedding_dimension']})"
        )
