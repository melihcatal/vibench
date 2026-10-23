import os
import openai
from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class AuditNote:
    """Audit note with embedding."""

    note_id: str
    text: str
    timestamp: str
    user: str
    action: str
    embedding: Optional[List[float]] = None


@dataclass
class SearchResult:
    """Search result with similarity score."""

    note_id: str
    text: str
    timestamp: str
    user: str
    action: str
    similarity: float


def embed_audit_notes(
    notes: List[Dict[str, Any]], model: str = "text-embedding-3-small"
) -> List[AuditNote]:
    """
    Embed secret audit notes for semantic search using OpenAI Embeddings.

    Args:
        notes: List of audit note dictionaries
        model: OpenAI embedding model to use

    Returns:
        List of AuditNote objects with embeddings
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    audit_notes = []

    for note in notes:
        text = note.get("text", "")
        if not text:
            continue

        try:
            response = client.embeddings.create(
                model=model, input=text, encoding_format="float"
            )

            embedding = response.data[0].embedding

            audit_note = AuditNote(
                note_id=note.get("id", ""),
                text=text,
                timestamp=note.get("timestamp", ""),
                user=note.get("user", ""),
                action=note.get("action", ""),
                embedding=embedding,
            )

            audit_notes.append(audit_note)

        except openai.OpenAIError as e:
            print(f"Error embedding note {note.get('id', 'unknown')}: {e}")
            audit_note = AuditNote(
                note_id=note.get("id", ""),
                text=text,
                timestamp=note.get("timestamp", ""),
                user=note.get("user", ""),
                action=note.get("action", ""),
            )
            audit_notes.append(audit_note)

    return audit_notes


def search_audit_notes(
    notes: List[AuditNote],
    query: str,
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> List[SearchResult]:
    """
    Search audit notes using semantic similarity.

    Args:
        notes: List of AuditNote objects (some may have embeddings)
        query: Search query text
        top_k: Number of results to return
        model: OpenAI embedding model to use

    Returns:
        List of SearchResult objects sorted by similarity
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=query, encoding_format="float"
        )
        query_embedding = np.array(response.data[0].embedding)
    except openai.OpenAIError as e:
        raise RuntimeError(f"Error embedding query: {e}") from e

    results = []

    for note in notes:
        if note.embedding is None:
            continue

        note_embedding = np.array(note.embedding)

        similarity = cosine_similarity(query_embedding, note_embedding)

        result = SearchResult(
            note_id=note.note_id,
            text=note.text,
            timestamp=note.timestamp,
            user=note.user,
            action=note.action,
            similarity=similarity,
        )

        results.append(result)

    results.sort(key=lambda x: x.similarity, reverse=True)

    return results[:top_k]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def cluster_audit_notes(
    notes: List[AuditNote], n_clusters: int = 3
) -> Dict[int, List[AuditNote]]:
    """
    Cluster audit notes based on embedding similarity.

    Args:
        notes: List of AuditNote objects with embeddings
        n_clusters: Number of clusters to create

    Returns:
        Dictionary mapping cluster ID to list of notes
    """
    from sklearn.cluster import KMeans

    notes_with_embeddings = [note for note in notes if note.embedding is not None]

    if len(notes_with_embeddings) < n_clusters:
        n_clusters = len(notes_with_embeddings)

    if n_clusters <= 1:
        return {0: notes_with_embeddings}

    embeddings = np.array([note.embedding for note in notes_with_embeddings])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings)

    clusters = {}
    for i, note in enumerate(notes_with_embeddings):
        cluster_id = int(cluster_labels[i])
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(note)

    return clusters
