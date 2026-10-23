import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_batch(texts: Sequence[str], model: str = "text-embedding-3-large") -> List[List[float]]:
    client = _get_client()
    response = client.embeddings.create(model=model, input=list(texts))
    embeddings = [item.embedding for item in response.data]
    return embeddings


def embed_batch_iter(texts: Iterable[str], model: str = "text-embedding-3-large") -> List[List[float]]:
    return embed_batch(list(texts), model=model)
