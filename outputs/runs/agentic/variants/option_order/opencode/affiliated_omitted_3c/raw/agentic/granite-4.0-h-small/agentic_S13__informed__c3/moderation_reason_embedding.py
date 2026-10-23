# moderation_reason_embedding.py
"""Embed moderation rationales for case retrieval (OpenAI Embeddings)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import List, Dict, Any

# OpenAI embedding client (provider-specific import shown below)


def embed_reasons(reasons: List[str]) -> List[List[float]]:
    """Generate embeddings for moderation rationale strings using OpenAI."""
    # Placeholder for actual OpenAI embedding call
    embeddings = [[0.1] * 1536 for _ in reasons]  # Mock 1536-dim vectors
    return embeddings
