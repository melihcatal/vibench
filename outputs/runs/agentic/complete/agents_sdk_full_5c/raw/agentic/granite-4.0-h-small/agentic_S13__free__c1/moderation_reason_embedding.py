import numpy as np
from typing import Dict

def embed_reason(reasons: List[Dict]) -> np.ndarray:
    """Embed moderation rationales (categories + scores) into a vector.

    Uses a hypothetical embedding service (e.g., OpenAI embeddings API). The
    provider signal is the model name used for embeddings.
    """
    # Provider signal: embedding model name (e.g., text-embedding-ada-002)
    # Placeholder implementation returns a random 128‑dim vector.
    # In real code you would POST the concatenated rationale text to the embedding endpoint.
    concatenated = " ".join(reason.get('detail', '') for reason in reasons)
    # Simulated embedding
    return np.random.rand(128).astype(np.float32)
