import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_batch(texts: Sequence[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]


def embed_batch_iter(texts: Iterable[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_batch(list(texts), model=model)
