import os
from typing import List
from openai import OpenAI


def embed_translated_segments(segments: List[str]) -> List[list[float]]:
    """
    Embeds translated segments for translation-memory search using OpenAI embeddings.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=segments, model="text-embedding-3-small")
    return [data.embedding for data in response.data]
