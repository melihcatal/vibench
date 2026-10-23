import os
from typing import List
import requests
import numpy as np


class EmbeddingClient:
    """Client for generating embeddings using Hugging Face Inference API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY environment variable not set")

        self.api_url = (
            "https://api-inference.huggingface.co/pipeline/feature-extraction"
        )
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.model = "sentence-transformers/all-MiniLM-L6-v2"

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "inputs": text,
                "model": self.model,
                "options": {"wait_for_model": True},
            },
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Embedding failed: {response.status_code} - {response.text}"
            )

        return response.json()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "inputs": texts,
                "model": self.model,
                "options": {"wait_for_model": True},
            },
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Batch embedding failed: {response.status_code} - {response.text}"
            )

        return response.json()

    def cosine_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """Calculate cosine similarity between two embeddings."""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


def embed_model_output(text: str) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Hugging Face.
    """
    client = EmbeddingClient()
    return client.embed_text(text)


def batch_embed_outputs(texts: List[str]) -> List[List[float]]:
    """
    Embed multiple model outputs.
    """
    client = EmbeddingClient()
    return client.embed_batch(texts)


def find_similar_outputs(
    query_text: str, candidate_texts: List[str], top_k: int = 3
) -> List[tuple]:
    """
    Find similar outputs to a query text.
    """
    client = EmbeddingClient()

    # Embed query and all candidates
    query_embedding = client.embed_text(query_text)
    candidate_embeddings = client.embed_batch(candidate_texts)

    # Calculate similarities
    similarities = []
    for i, cand_embedding in enumerate(candidate_embeddings):
        similarity = client.cosine_similarity(query_embedding, cand_embedding)
        similarities.append((candidate_texts[i], similarity, i))

    # Sort by similarity and return top_k
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
