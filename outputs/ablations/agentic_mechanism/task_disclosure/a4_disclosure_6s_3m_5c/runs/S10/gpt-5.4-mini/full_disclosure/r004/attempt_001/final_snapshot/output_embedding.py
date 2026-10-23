import os
from typing import List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_output(text: str, model: str = "text-embedding-3-small") -> List[float]:
    response = _client().embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)


def embed_outputs(texts: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    response = _client().embeddings.create(model=model, input=list(texts))
    return [list(item.embedding) for item in response.data]
