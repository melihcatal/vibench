"""
Embed moderation rationales for case retrieval using Cohere Embed API.
"""
import os
import cohere
from typing import List


def embed_moderation_reason(text: str) -> List[float]:
    """Embed moderation rationale using Cohere."""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[text], model="embed-english-v3.0")
    return response.embeddings[0]