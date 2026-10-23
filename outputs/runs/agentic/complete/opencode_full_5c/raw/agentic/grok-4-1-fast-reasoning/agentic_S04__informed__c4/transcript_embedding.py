import os
from openai import OpenAI
from typing import List


def transcript_embedding(
    segments: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=model,
        input=segments,
    )
    return [data.embedding for data in response.data]
