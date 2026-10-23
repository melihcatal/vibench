import os
from typing import Dict, Any

# Using Anthropic for embedding (requires ANTHROPIC_API_KEY env var)
import anthropic

def create_embedding(secret_id: str, note: str) -> str:
    """Generate a text embedding of a secret audit note for semantic search.

    Args:
        secret_id: Identifier of the secret (used as metadata).
        note: Human‑written audit comment.

    Returns:
        A base64‑encoded embedding vector (Anthropic returns it directly).
    """
    client = anthropic.Anthropic()
    # Use the 'text-embedding' model (or the default if omitted)
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": note}],
        response_format={"type": "embedding"}
    )
    # The embedding is a list of floats; we encode as JSON string
    return str(response.embedding)  # type: ignore
