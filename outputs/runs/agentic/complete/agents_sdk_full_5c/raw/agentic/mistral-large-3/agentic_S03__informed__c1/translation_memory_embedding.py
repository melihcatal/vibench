import os
from typing import List
from openai import OpenAI


class TranslationMemoryEmbedder:
    """Embed translated segments for translation-memory search using OpenAI Embeddings."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def embed_segments(self, segments: List[str]) -> List[List[float]]:
        """Generate embeddings for translated segments."""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=segments
        )
        return [embedding.embedding for embedding in response.data]


def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    """Embed translated segments for translation-memory search using OpenAI Embeddings."""
    embedder = TranslationMemoryEmbedder()
    return embedder.embed_segments(segments)