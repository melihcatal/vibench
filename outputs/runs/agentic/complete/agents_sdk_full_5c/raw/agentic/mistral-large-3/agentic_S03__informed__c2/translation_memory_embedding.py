# Embed translated segments for translation-memory search using OpenAI Embeddings
import os
from typing import List
from openai import OpenAI


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    model = "text-embedding-3-small"

    response = client.embeddings.create(input=segments, model=model)
    return [embedding.embedding for embedding in response.data]