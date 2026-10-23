import os
import cohere
from typing import Dict, Any


def crypto_audit_embedding(text: str) -> Dict[str, Any]:
    """
    Embeds crypto audit notes for semantic search using Cohere Embeddings.

    Args:
        text: Crypto audit notes or logs to embed.

    Returns:
        Dictionary containing embedding vector and metadata.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key must be set.")

    co = cohere.Client(api_key)
    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    return {
        "embedding": response.embeddings[0],
        "text": text,
        "model": "embed-english-v3.0",
    }
