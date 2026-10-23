from typing import List

from openai import OpenAI


def caption_embedding(captions: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=captions)
    return [item.embedding for item in response.data]
