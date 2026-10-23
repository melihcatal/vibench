import os
from functools import lru_cache

from openai import OpenAI


def embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_text(value: str) -> str:
    return " ".join((value or "").split())


def embed_inputs(inputs):
    client = get_client()
    return client.embeddings.create(model=embedding_model(), input=inputs)
