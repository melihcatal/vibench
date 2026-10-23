import os
from typing import List
from openai import OpenAI


def embed_transcript_segments(
    segments: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=segments, model=model)
    return [datum.embedding for datum in response.data]
