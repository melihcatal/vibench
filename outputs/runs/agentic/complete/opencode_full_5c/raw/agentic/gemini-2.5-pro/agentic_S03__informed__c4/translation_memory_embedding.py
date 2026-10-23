import os
from typing import List
from openai import OpenAI


def translation_memory_embedding(translated_segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    if not translated_segments:
        return []

    response = client.embeddings.create(
        input=translated_segments, model="text-embedding-3-small"
    )

    return [embedding.embedding for embedding in response.data]
