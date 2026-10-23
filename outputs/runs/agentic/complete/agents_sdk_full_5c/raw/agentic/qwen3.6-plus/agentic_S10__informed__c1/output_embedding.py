"""
Embed model outputs for clustering or retrieval using OpenAI Embeddings API.
Provider: OpenAI Embeddings API (model: text-embedding-3-small)
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
from typing import List, Optional, Dict, Any
from model_client import get_client, EMBEDDING_MODEL


class OpenAIEmbedder:
    """Client for OpenAI Embeddings API for text vectorization."""

    def __init__(self, model: str = EMBEDDING_MODEL):
        self.model = model
        self.client = get_client()

    def embed_text(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        """
        Generate an embedding vector for a single text.

        Args:
            text: The text to embed.
            model: OpenAI embedding model identifier (e.g., "text-embedding-3-small").

        Returns:
            List of floats representing the embedding vector.
        """
        model_id = model or self.model
        response = self.client.create_embedding(text=text, model=model_id)
        return response.data[0].embedding

    def embed_texts(
        self,
        texts: List[str],
        model: Optional[str] = None,
        batch_size: int = 100,
    ) -> List[List[float]]:
        """
        Generate embedding vectors for multiple texts.

        Args:
            texts: List of texts to embed.
            model: OpenAI embedding model identifier.
            batch_size: Maximum number of texts per API call.

        Returns:
            List of embedding vectors, one per input text.
        """
        model_id = model or self.model
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.client.embeddings.create(
                model=model_id,
                input=batch,
            )
            # Sort by index to ensure order matches input
            sorted_data = sorted(response.data, key=lambda x: x.index)
            batch_embeddings = [item.embedding for item in sorted_data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def compute_similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:
        """
        Compute cosine similarity between two texts.

        Args:
            text1: First text.
            text2: Second text.

        Returns:
            Cosine similarity score between 0 and 1.
        """
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)
        return cosine_similarity(emb1, emb2)

    def find_most_similar(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find the most similar candidates to a query text.

        Args:
            query: The query text.
            candidates: List of candidate texts.
            top_k: Number of top results to return.

        Returns:
            List of dicts with candidate text, index, and similarity score.
        """
        query_embedding = self.embed_text(query)
        candidate_embeddings = self.embed_texts(candidates)

        similarities = []
        for i, cand_emb in enumerate(candidate_embeddings):
            sim = cosine_similarity(query_embedding, cand_emb)
            similarities.append({
                "index": i,
                "text": candidates[i],
                "similarity": sim,
            })

        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    import math
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def embed_output(
    text: str,
    model: str = EMBEDDING_MODEL,
) -> List[float]:
    """
    Quick function to embed a single text output.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier.

    Returns:
        Embedding vector as a list of floats.
    """
    embedder = OpenAIEmbedder(model=model)
    return embedder.embed_text(text)


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY environment variable is required.")
    else:
        embedder = OpenAIEmbedder()
        texts = [
            "The quick brown fox jumps over the lazy dog.",
            "A fast brown fox leaps above a sleepy canine.",
            "Python is a popular programming language.",
        ]
        query = "A swift fox jumping over a resting dog."
        results = embedder.find_most_similar(query, texts, top_k=2)
        print(f"Query: {query}")
        for r in results:
            print(f"  [{r['similarity']:.4f}] {r['text']}")
