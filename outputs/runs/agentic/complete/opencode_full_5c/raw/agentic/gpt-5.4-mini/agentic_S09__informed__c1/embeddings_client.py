import os
from functools import lru_cache
from typing import Any

from openai import OpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_input(input_data: Any):
    client = get_openai_client()
    return client.embeddings.create(model=get_embedding_model(), input=input_data)
