import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_outputs(outputs: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    if not outputs:
        return []
    client = _client()
    response = client.embeddings.create(model=model, input=list(outputs))
    return [item.embedding for item in response.data]


def embed_output(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_outputs([text], model=model)
    return embeddings[0] if embeddings else []


def clusterable_embedding_payload(outputs: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_outputs(list(outputs), model=model)
