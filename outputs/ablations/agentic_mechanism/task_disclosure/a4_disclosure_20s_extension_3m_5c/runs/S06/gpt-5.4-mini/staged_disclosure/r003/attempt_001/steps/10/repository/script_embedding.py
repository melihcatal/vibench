import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_scripts(scripts: Sequence[str]) -> List[List[float]]:
    client = _client()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(scripts))
    return [item.embedding for item in response.data]


def embed_script(script: str) -> List[float]:
    return embed_scripts([script])[0]


def batch_embed_scripts(scripts: Iterable[str], batch_size: int = 96) -> List[List[float]]:
    items = list(scripts)
    embeddings: List[List[float]] = []
    for start in range(0, len(items), batch_size):
        embeddings.extend(embed_scripts(items[start : start + batch_size]))
    return embeddings
