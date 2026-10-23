import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not texts:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
