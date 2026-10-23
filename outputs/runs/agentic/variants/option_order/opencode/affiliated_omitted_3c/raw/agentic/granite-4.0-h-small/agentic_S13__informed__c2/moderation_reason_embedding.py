import json
from safety_client import SafetyClient


def embed_reason(reason: str, model_name: str = "text-embedding") -> list[float]:
    """Embed a moderation rationale using DashScope embeddings.

    Returns a list of floats representing the vector.
    """
    client = SafetyClient()
    # Placeholder call; DashScope SDK would return a vector
    vector = [0.1, 0.2, 0.3, 0.4]  # mock 4‑dimensional embedding
    return vector
