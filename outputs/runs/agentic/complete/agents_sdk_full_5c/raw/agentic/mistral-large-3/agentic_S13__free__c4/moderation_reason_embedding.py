"""
Embed moderation rationales for case retrieval using Cohere's embedding API.
"""
import os
from typing import List
import cohere
from safety_models import TextModerationResult


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """Embed moderation rationales using Cohere's embedding API."""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    if not co:
        raise ValueError("COHERE_API_KEY environment variable is required.")

    response = co.embed(
        model="large",
        texts=reasons
    )
    return response.embeddings