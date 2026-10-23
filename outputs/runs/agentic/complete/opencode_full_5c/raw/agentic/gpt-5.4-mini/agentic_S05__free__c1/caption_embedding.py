from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=list(chunks),
    )
    return [item.embedding for item in response.data]
