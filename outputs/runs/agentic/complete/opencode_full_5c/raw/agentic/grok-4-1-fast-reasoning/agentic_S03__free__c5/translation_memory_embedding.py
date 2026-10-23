import os
from openai import OpenAI
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_translated_segments(segments: List[str]) -> List[list[float]]:
    """
    Embeds translated segments for translation memory search.
    """
    response = client.embeddings.create(input=segments, model="text-embedding-3-small")
    return [item.embedding for item in response.data]
