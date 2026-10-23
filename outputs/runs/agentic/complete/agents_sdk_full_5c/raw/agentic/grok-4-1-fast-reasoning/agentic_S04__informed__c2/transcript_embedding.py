import os
from openai import OpenAI
from typing import List

def transcript_embedding(segments: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=segments
    )
    return [embedding.embedding for embedding in response.data]
