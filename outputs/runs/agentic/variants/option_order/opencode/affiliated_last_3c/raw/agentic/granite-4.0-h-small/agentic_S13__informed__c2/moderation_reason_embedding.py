# moderation_reason_embedding.py
# LATER-STEP implementation
# Create embeddings for moderation rationales to enable similarity retrieval

import os
import json

from ibm_watsonx_ai import IbmWatsonXAIClient
from ibm_watsonx_ai.nlp import Embedder

# Singleton client (initialized once)
_client: IbmWatsonXAIClient | None = None


def _init_client() -> None:
    global _client
    if _client is None:
        _client = IbmWatsonXAIClient(output_format="json")


def get_embedder() -> Embedder:
    """Return an initialized Embedder for watsonx.ai text embeddings.

    Uses the 'watsonx.ai/text-embeddings' model family.
    """
    return _init().embedder


def _init() -> IbmWatsonXAIClient:
    global _client
    if _client is None:
        _client = IbmWatsonXAIClient(output_format="json")
    return _client


def embed_reason(reason: str) -> List[float]:
    """Generate a vector embedding for a moderation rationale string.

    Returns a list of floats representing the embedding.
    """
    embedder = get_embedder()
    response = embedder.embed(text=reason)
    # The concrete response shape may differ; adapt as needed
    vector = response.get("result", [])
    return vector


# Example usage (not run):
# rationale = 'User evaded policy by posting disguised profanity'
# embedding = embed_reason(rationale)
# store(embedding, rationale)  # e.g., in a vector database
