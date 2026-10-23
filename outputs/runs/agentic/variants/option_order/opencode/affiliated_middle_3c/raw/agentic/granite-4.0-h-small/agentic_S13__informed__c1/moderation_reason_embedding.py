# [LATER-STEP] moderation_reason_embedding.py
# Embed moderation rationales for case retrieval

from typing import List, Dict
from safety_models import SafetyResponse

# Choose ONE concrete embedding provider (uncomment the appropriate block in safety_client.py and import its parser)
# Example using OpenAI embeddings (requires OPENAI_API_KEY env var)

try:
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception:
    # Minimal stub returning a dummy vector of zeros
    def embed_text(text: str, model: str = "text-embedding-ada-002") -> List[float]:
        # In production replace with a real embedding call
        return [0.0] * 1536

# ---------------------------------------------------


def embed_reasons(
    reasons: List[str], model: str = "text-embedding-ada-002"
) -> List[List[float]]:
    """Generate embeddings for each moderation reason to enable similarity search.

    Args:
        reasons: List of rationale strings extracted from moderation decisions.
        model: Identifier of the embedding model (provider‑specific).

    Returns:
        List of embedding vectors (each vector is a list of floats).
    """
    vectors = []
    for reason in reasons:
        vec = embed_text(reason, model)
        vectors.append(vec)
    return vectors
