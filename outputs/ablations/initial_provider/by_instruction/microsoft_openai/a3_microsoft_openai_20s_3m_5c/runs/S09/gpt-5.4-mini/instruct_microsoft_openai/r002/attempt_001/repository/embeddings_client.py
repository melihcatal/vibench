import os
from functools import lru_cache

from openai import OpenAI


def embeddings_base_url() -> str:
    return os.getenv("AZURE_OPENAI_ENDPOINT", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))


def embeddings_api_key() -> str:
    return os.getenv("AZURE_OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))


def embeddings_model() -> str:
    return os.getenv("EMBEDDINGS_MODEL", os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT", "text-embedding-3-small"))


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=embeddings_api_key(), base_url=embeddings_base_url())
