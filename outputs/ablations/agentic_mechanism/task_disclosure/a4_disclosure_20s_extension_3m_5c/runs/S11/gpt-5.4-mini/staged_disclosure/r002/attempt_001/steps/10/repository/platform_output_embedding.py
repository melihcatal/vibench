import os
from typing import List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_platform_outputs(outputs: Sequence[str]) -> List[List[float]]:
    if not outputs:
        return []
    client = _client()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(outputs))
    vectors = [item.embedding for item in response.data]
    return vectors


def embed_platform_output(output: str) -> List[float]:
    return embed_platform_outputs([output])[0]
