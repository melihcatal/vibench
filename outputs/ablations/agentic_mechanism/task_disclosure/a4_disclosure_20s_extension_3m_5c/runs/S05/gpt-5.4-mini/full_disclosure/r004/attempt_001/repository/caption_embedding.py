import os
from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts = [chunk for chunk in chunks if chunk is not None and str(chunk).strip()]
    if not texts:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
