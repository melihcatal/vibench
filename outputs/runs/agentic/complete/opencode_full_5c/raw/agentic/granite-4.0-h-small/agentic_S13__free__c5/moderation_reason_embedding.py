# [LATER-STEP] moderation_reason_embedding.py
# Embed moderation rationales for case retrieval

from sentence_transformers import SentenceTransformer
import torch


def embed_reason(reason: str, model_name: str = "all-MiniLM-L6-v2") -> torch.Tensor:
    """Return embedding vector for a moderation rationale string."""
    model = SentenceTransformer(model_name)
    # SentenceTransformer returns a torch tensor
    return model.encode(reason, convert_to_tensor=True)
