from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from .embeddings_client import create_client, normalize_response

@dataclass
class EmbedRequest:
    """Configuration for embedding request.

    Args:
        texts: List of strings to embed.
        model_id: Optional model identifier.
        normalize: Whether to L2-normalize the returned vectors.
    """
    texts: List[str]
    model_id: Optional[str] = None
    normalize: bool = True


def embed_text(text: str, model_id: Optional[str] = None) -> List[float]:
    """Single text embedding via the provider.

    Args:
        text: The text.
        model_id: Specific model if desired.
    Returns:
        List[float] embedding vector.
    """
    request = EmbedRequest(texts=[text], model_id=model_id)
    return _embed_batch(request, normalize=request.normalize)[0]


def embed_batch(texts: List[str], model_id: Optional[str] = None) -> List[List[float]]:
    """Batch embedding request.

    Args:
        texts: Iterable of strings.
        model_id: Optional model.
    Returns:
        List of embedding vectors, one per input.
    """
    request = EmbedRequest(texts=list(texts), model_id=model_id)
    return _embed_batch(request, normalize=request.normalize)


def _embed_batch(request: EmbedRequest, normalize: bool) -> List[List[float]]:
    client = create_client()
    # Build payload for IBM Watsonx embeddings endpoint
    payload = {
        "input": request.texts,
        "model": request.model_id or "embed-ada-002"
    }
    response = client.create_embeddings(payload)  # type: ignore
    vectors = normalize_response(response) if normalize else response
    return vectors

# Utility to map model name to Watsonx model identifier (extend as needed)
def resolve_model_id(model_id: Optional[str]) -> str:
    """Map a generic model alias to Watsonx model ID.

    Default: embed-ada-002 (OpenAI-like model)."
    aliases = {
        "openai": "embed-ada-002",
        "cohere": "cohere-embed",
        "gemini": "gemini-embed",
    }
    return aliases.get(model_id, model_id or "embed-ada-002")
