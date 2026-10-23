import os
from typing import List

from openai import OpenAI


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=segments,
    )
    return [item.embedding for item in response.data]
