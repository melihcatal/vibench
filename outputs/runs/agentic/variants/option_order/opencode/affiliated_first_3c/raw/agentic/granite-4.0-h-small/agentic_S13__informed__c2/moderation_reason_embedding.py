import os
import numpy as np
from safety_client import get_client
from safety_models import ModerationRequest, moderate_text

# LATER-STEP
# Embed moderation rationales for case retrieval using a vector store.
# Provider identification: DASHSCOPE (DashScope embeddings)


def embed_reason(reason: str) -> np.ndarray:
    """
    Returns a numpy vector representation of the moderation rationale.
    """
    client = get_client("dashscope")
    # DashScope embeddings endpoint
    response = client.text_embedding(
        model="Qwen2-14B",
        texts=[reason],
    )
    # Embeddings are returned as list of floats
    return np.array(response.embeddings[0])
