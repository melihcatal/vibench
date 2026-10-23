import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_outputs(outputs: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    if not outputs:
        return []
    response = _client().embeddings.create(model=model, input=list(outputs))
    return [item.embedding for item in response.data]


def embed_output(output: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return embed_outputs([output], model=model)[0]


def pairwise_embeddings(outputs: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_outputs(list(outputs), model=model)
