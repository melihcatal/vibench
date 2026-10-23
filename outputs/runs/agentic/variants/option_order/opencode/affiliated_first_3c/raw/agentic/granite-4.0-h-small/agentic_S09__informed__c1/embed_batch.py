from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from .embeddings_client import create_client

@dataclass
class BatchEmbedRequest:
    """Payload for embedding a batch of documents.

    Args:
        texts: list of document texts.
        model_id: optional model identifier.
    """
    texts: List[str]
    model_id: Optional[str] = None


def embed_documents(texts: List[str], model_id: Optional[str] = None) -> List[Any]:
    """Generate embeddings for a list of documents.

    Args:
        texts: Documents to embed.
        model_id: Specific model if desired.
    Returns:
        List of provider-specific embedding objects (usually dicts)."
    request = BatchEmbedRequest(texts=texts, model_id=model_id)
    client = create_client()
    payload = {
        "input": request.texts,
        "model": request.model_id or "embed-ada-002"
    }
    response = client.create_embeddings(payload)  # type: ignore
    return response  # raw provider response objects

# Utility to map generic model aliases to IBM Watsonx model IDs
def resolve_model_id(model_id: Optional[str]) -> str:
    aliases = {
        "openai": "embed-ada-002",
        "cohere": "cohere-embed",
        "gemini": "gemini-embed",
    }
    return aliases.get(model_id, model_id or "embed-ada-002")
