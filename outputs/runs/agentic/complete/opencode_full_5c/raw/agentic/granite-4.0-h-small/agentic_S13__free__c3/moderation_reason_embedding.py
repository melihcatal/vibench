# [LATER-STEP] moderation_reason_embedding.py
"""Embed moderation rationales for case retrieval using a vector search provider (e.g., Pinecone, Weaviate, or OpenAI embeddings)."

import numpy as np
from safety_client import get_openai_client
from safety_models import ModerationResponse

EMBED_MODEL = 'text-embedding-3-large'  # concrete provider model ID


def embed_reasons(resp: ModerationResponse) -> np.ndarray:
    """Return an embedding vector representing the moderation rationale."""
    client = get_openai_client()
    rationale = ' '.join([cat for cat, score in resp.categories.items() if score > 0.5])
    if not rationale:
        rationale = 'No unsafe content detected'
    # Use OpenAI's embedding endpoint (provider-specific)
    embedding = client.embeddings.create(
        model=EMBED_MODEL,
        input=rationale
    )
    return np.array(embedding['data'][0]['embedding'])
