import os
from openai import OpenAI
from typing import List


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=segments, model="text-embedding-3-small")
    return [data.embedding for data in response.data]
