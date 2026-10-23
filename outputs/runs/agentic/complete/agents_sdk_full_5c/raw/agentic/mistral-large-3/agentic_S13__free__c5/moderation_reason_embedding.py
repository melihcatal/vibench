import os
from typing import List, Optional
from sentence_transformers import SentenceTransformer


class ModerationReasonEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_reason(self, reason: str) -> List[float]:
        return self.model.encode(reason, convert_to_tensor=False).tolist()


def embed_moderation_reason(reason: str) -> List[float]:
    embedder = ModerationReasonEmbedder()
    return embedder.embed_reason(reason)