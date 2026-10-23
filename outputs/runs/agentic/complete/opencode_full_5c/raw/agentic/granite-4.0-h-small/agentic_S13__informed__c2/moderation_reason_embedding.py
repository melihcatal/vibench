# [LATER-STEP] moderation_reason_embedding.py
"""Embed moderation rationales for case retrieval using Alibaba Text Embedding SDK.
Creates an embedding vector for the moderation reason text to enable similarity search.
"""

import os
from dashscope import EmbeddingClient  # provider: DashScope embeddings
from safety_client import normalize_response


async def embed_reason(reason: str) -> list[float]:
    """Return a dense vector (list of floats) for the provided moderation reason."""
    client = EmbeddingClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
    response = client.embeddings(
        system="text", model_id="text-embedding-ada-002", input_text=reason
    )
    # Assuming the API returns a list of floats under 'embedding'
    return response["embedding"]
