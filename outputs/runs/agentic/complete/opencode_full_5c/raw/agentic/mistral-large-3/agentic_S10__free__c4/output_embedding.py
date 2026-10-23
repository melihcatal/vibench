import os
from typing import List, Optional, Dict, Any
from sentence_transformers import SentenceTransformer
from model_client import get_llm_client


class OutputEmbedder:
    """
    Embeds model outputs for clustering or retrieval using Sentence Transformers.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float]:
        """
        Embeds the provided text into a vector.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        return self.model.encode(text).tolist()


def embed_output(text: str) -> List[float]:
    """
    Embeds model output for clustering or retrieval.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    embedder = OutputEmbedder()
    return embedder.embed(text)
