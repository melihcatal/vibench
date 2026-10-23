from openai import OpenAI
import numpy as np
from typing import List, Dict, Any
import os

# Provider: OpenAI Embeddings
# Model: text-embedding-3-small


def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using OpenAI Embeddings.

    Args:
        segments: A list of translated text segments.

    Returns:
        A list of embedding vectors for the segments.
    """
    if not segments:
        return []

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(input=segments, model="text-embedding-3-small")

    return [embedding.embedding for embedding in response.data]
