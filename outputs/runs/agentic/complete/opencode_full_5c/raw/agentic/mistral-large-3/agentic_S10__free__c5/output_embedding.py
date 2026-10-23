from typing import Optional, List, Dict, Any
import os
import numpy as np
from sentence_transformers import SentenceTransformer


class OutputEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float]:
        """
        Embed model outputs for clustering or retrieval using SentenceTransformers.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()


def get_output_embedder(model_name: Optional[str] = None) -> OutputEmbedder:
    """
    Initialize and return an output embedder using SentenceTransformers.
    """
    return OutputEmbedder(model_name=model_name or "all-MiniLM-L6-v2")
