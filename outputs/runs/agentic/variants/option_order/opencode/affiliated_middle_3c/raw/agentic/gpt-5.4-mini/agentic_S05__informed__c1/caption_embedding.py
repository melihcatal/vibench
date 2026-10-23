import os
from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        input=list(chunks),
    )
    return [item.embedding for item in response.data]
