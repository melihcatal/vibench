from typing import Iterable, List

from openai import OpenAI


def caption_embedding(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    resp = client.embeddings.create(model="text-embedding-3-small", input=list(chunks))
    return [item.embedding for item in resp.data]
