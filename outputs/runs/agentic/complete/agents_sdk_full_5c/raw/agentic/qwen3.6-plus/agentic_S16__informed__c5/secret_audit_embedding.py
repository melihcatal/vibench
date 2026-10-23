"""Embed secret audit notes for semantic search using Cohere Embed API."""

import os
from typing import Any
import cohere


def embed_secret_audit_notes(
    notes: list[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
) -> dict[str, Any]:
    """Generate embeddings for secret audit notes using Cohere.

    Args:
        notes: A list of audit note strings to embed.
        model: Cohere embedding model identifier, defaults to 'embed-english-v3.0'.
        input_type: Input type for the embedding model. Valid values include
            'search_document', 'search_query', 'classification', 'clustering'.

    Returns:
        A dict with 'embeddings' (list of float lists), 'model', and 'count'.

    Raises:
        ValueError: If COHERE_API_KEY is not set.
        Exception: If the Cohere API call fails.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    client = cohere.Client(api_key=api_key)

    response = client.embed(
        texts=notes,
        model=model,
        input_type=input_type,
    )

    return {
        "embeddings": response.embeddings,
        "model": model,
        "count": len(response.embeddings),
        "input_type": input_type,
    }


def embed_audit_notes_for_search(
    notes: list[dict[str, Any]],
    text_field: str = "note_text",
) -> list[tuple[dict[str, Any], list[float]]]:
    """Embed audit notes and pair them with their original metadata.

    Args:
        notes: A list of audit note dicts (e.g., from security_models.AuditNote).
        text_field: The key containing the text to embed.

    Returns:
        A list of (metadata_dict, embedding_vector) tuples.
    """
    texts = [note.get(text_field, "") for note in notes]
    result = embed_secret_audit_notes(texts)

    paired = []
    for i, note in enumerate(notes):
        embedding = result["embeddings"][i] if i < len(result["embeddings"]) else []
        paired.append((note, embedding))
    return paired


if __name__ == "__main__":
    sample_notes = [
        "Rotated DB password after quarterly review",
        "API key rotated due to potential exposure in logs",
        "Certificate secret renewed before expiration",
    ]
    result = embed_secret_audit_notes(sample_notes)
    print(f"Embedded {result['count']} notes using model {result['model']}")
    if result["embeddings"]:
        print(f"Embedding dimension: {len(result['embeddings'][0])}")
