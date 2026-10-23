import os
import requests

# Embed moderation rationales using Anthropic's embeddings endpoint
EMBED_ENDPOINT = os.getenv(
    "ANTHROPIC_EMBED_ENDPOINT", "https://api.anthropic.com/v1/embeddings"
)
EMBED_API_KEY = os.getenv("ANTHROPIC_EMBED_API_KEY")

EMBEDDING_ERROR = []  # default placeholder embedding


def embed_moderation_reason(reason_text: str) -> list[float]:
    """Create a dense vector embedding for the moderation rationale text."""
    if not EMBED_API_KEY:
        raise RuntimeError("ANTHROPIC_EMBED_API_KEY environment variable not set")
    payload = {"model": "claude-3-embed-20240229", "input": reason_text}
    response = requests.post(
        EMBED_ENDPOINT, json=payload, headers={"x-api-key": EMBED_API_KEY}, timeout=10
    )
    response.raise_for_status()
    # Anthropic embeddings are returned as a list of floats in the \"embedding\" field
    return (
        response.json()["embedding"]
        if response.json().get("embedding")
        else EMBEDDING_ERROR
    )
