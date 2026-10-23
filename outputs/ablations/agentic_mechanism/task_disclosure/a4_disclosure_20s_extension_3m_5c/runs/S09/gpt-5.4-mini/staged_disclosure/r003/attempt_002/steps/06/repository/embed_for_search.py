import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_texts(texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    if not texts:
        return []
    response = _client().embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]


def embed_query(query: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return embed_texts([query], model=model)[0]


def embed_documents(documents: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_texts(list(documents), model=model)
