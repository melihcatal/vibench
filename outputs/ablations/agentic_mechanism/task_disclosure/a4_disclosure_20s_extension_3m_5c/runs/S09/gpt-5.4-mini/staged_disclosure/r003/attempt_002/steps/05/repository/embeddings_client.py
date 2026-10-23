import os
from typing import Iterable, List, Optional, Sequence

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)


def embed_text(text: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> List[float]:
    api_client = client or get_client()
    response = api_client.embeddings.create(model=model or get_embedding_model(), input=text)
    return response.data[0].embedding


def embed_texts(
    texts: Sequence[str],
    *,
    client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> List[List[float]]:
    api_client = client or get_client()
    response = api_client.embeddings.create(model=model or get_embedding_model(), input=list(texts))
    return [item.embedding for item in response.data]


def embed_iterable(
    texts: Iterable[str],
    *,
    client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> List[List[float]]:
    return embed_texts(list(texts), client=client, model=model)
