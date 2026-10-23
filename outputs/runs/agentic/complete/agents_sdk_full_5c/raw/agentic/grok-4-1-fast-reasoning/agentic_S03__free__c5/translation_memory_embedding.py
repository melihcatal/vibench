import os
from typing import List
from openai import OpenAI

def embed_translated_segments(segments: List[str]) -> List[list[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=segments,
        model="text-embedding-3-small",
    )
    return [datum.embedding for datum in response.data]
