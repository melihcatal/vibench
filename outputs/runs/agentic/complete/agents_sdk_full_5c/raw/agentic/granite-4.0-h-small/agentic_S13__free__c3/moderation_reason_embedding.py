import os
from sentence_transformers import SentenceTransformer
from typing import Dict
# Load a small general-purpose model (no HuggingFace Hub auth needed)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_reason(reason: str) -> List[float]:
    """Embed a moderation rationale sentence into a vector."""
    return model.encode(reason, convert_to_tensor=False)

# Example: build embeddings for all reasons in a batch
def embed_reasons(reasons: List[str]) -> Dict[str, List[float]]:
    return {r: embed_reason(r) for r in reasons}
