import os
from typing import List, Dict, Any
import cohere
from security_models import CryptoAuditNote


def embed_crypto_audit_notes(notes: List[CryptoAuditNote]) -> List[Dict[str, Any]]:
    """
    Embed crypto audit notes for semantic search using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set")

    if not notes:
        return []

    client = cohere.Client(api_key)

    # Prepare texts for embedding
    texts = []
    for note in notes:
        # Create a comprehensive text representation of the note
        text = f"""
        Audit Note: {note.note_id}
        Operation: {note.operation}
        Key ID: {note.key_id}
        Severity: {note.severity}
        Tags: {", ".join(note.tags) if note.tags else "none"}
        Note: {note.note_text}
        Time: {note.timestamp.isoformat()}
        """
        texts.append(text.strip())

    try:
        # Get embeddings from Cohere
        response = client.embed(
            texts=texts, model="embed-english-v3.0", input_type="search_document"
        )

        embeddings = response.embeddings

        # Combine notes with their embeddings
        results = []
        for i, (note, embedding) in enumerate(zip(notes, embeddings)):
            results.append(
                {
                    "note_id": note.note_id,
                    "embedding": embedding,
                    "metadata": {
                        "operation": note.operation,
                        "key_id": note.key_id,
                        "severity": note.severity,
                        "tags": note.tags,
                        "timestamp": note.timestamp.isoformat(),
                        "text_preview": note.note_text[:100] + "..."
                        if len(note.note_text) > 100
                        else note.note_text,
                    },
                    "provider": "cohere",
                    "model": "embed-english-v3.0",
                    "embedding_dimensions": len(embedding),
                }
            )

        return results

    except Exception as e:
        # Return notes without embeddings in case of error
        return [
            {
                "note_id": note.note_id,
                "embedding": None,
                "metadata": {
                    "operation": note.operation,
                    "key_id": note.key_id,
                    "severity": note.severity,
                    "tags": note.tags,
                    "timestamp": note.timestamp.isoformat(),
                    "text_preview": note.note_text[:100] + "..."
                    if len(note.note_text) > 100
                    else note.note_text,
                },
                "error": str(e),
                "provider": "cohere",
            }
            for note in notes
        ]


def search_similar_notes(
    query: str, embedded_notes: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar crypto audit notes using Cohere embeddings.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set")

    if not embedded_notes:
        return []

    client = cohere.Client(api_key)

    try:
        # Get query embedding
        query_response = client.embed(
            texts=[query], model="embed-english-v3.0", input_type="search_query"
        )

        query_embedding = query_response.embeddings[0]

        # Calculate cosine similarity (simplified)
        # In production, use a proper vector database
        scored_notes = []
        for note in embedded_notes:
            if note.get("embedding") is None:
                continue

            # Simple cosine similarity
            import numpy as np

            emb1 = np.array(query_embedding)
            emb2 = np.array(note["embedding"])

            # Normalize
            emb1_norm = emb1 / np.linalg.norm(emb1)
            emb2_norm = emb2 / np.linalg.norm(emb2)

            similarity = np.dot(emb1_norm, emb2_norm)

            scored_notes.append({**note, "similarity_score": float(similarity)})

        # Sort by similarity score (descending)
        scored_notes.sort(key=lambda x: x["similarity_score"], reverse=True)

        return scored_notes[:top_k]

    except Exception as e:
        return [{"error": str(e), "provider": "cohere"}]
