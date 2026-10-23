# LATER-STEP: moderation_reason_embedding.py
"""Embed moderation rationales for case retrieval or similarity search."""

import os
import numpy as np
from typing import List, Dict

# Placeholder for a vector/embedding provider (e.g., OpenAI embeddings, Cohere, HuggingFace)
EMBED_PROVIDER = os.getenv("TEXT_EMBED_PROVIDER", "openai")
EMBED_API_KEY = os.getenv("TEXT_EMBED_API_KEY")


def embed_reasons(reasons: List[str]) -> List[np.ndarray]:
    """Generate embeddings for each moderation rationale provided in 'reasons'.

    Args:
        reasons: List of textual explanations from moderation reviews.

    Returns:
        List of numpy arrays, each representing an embedding vector.
    """
    if not EMBED_API_KEY:
        raise RuntimeError("TEXT_EMBED_API_KEY environment variable must be set")

    if EMBED_PROVIDER == "openai":
        # OpenAI embeddings endpoint example (stub)
        try:
            import openai

            openai.api_key = EMBED_API_KEY
            embeddings = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=reasons,
            )
            # embeddings['data'] contains a list of embedding dicts
            return [
                np.array(e["embedding"], dtype=np.float32) for e in embeddings["data"]
            ]
        except Exception as e:
            raise RuntimeError("OpenAI embedding failed") from e
    elif EMBED_PROVIDER == "cohere":
        # Cohere Generate endpoint example (stub)
        raise NotImplementedError("Cohere provider not implemented")
    else:
        raise RuntimeError(f"Unsupported embedding provider: {EMBED_PROVIDER}")
