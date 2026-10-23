import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import normalize_chunks


def embed_captions(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    texts = normalize_chunks(chunks)
    if not texts:
        return []
    response = client.embeddings.create(model="text-embedding-3-large", input=texts)
    return [item.embedding for item in response.data]
