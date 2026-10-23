import os
from sentence_transformers import SentenceTransformer

def embed_reason(reason: str, model_name: str = "all-MiniLM-L6-v2") -> list[float]:
    """Embed a moderation rationale (e.g., reason string) using a SentenceTransformer model.

    Args:
        reason: Human-readable explanation of a moderation decision.
        model_name: HuggingFace model identifier (default: all-MiniLM-L6-v2).

    Returns:
        List of floats representing the embedding vector.
    """
    # The model name identifes the concrete provider (SentenceTransformer/MSR) and model.
    model = SentenceTransformer(model_name)
    return model.encode(reason, convert_to_tensor=True).tolist()
