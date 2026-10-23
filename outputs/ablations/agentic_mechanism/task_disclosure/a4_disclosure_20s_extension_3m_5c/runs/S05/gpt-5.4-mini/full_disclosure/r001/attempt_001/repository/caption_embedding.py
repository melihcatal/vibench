import os
from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]
