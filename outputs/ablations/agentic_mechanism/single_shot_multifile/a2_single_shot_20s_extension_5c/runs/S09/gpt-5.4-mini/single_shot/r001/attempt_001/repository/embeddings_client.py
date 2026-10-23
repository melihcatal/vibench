import os
from functools import lru_cache
from openai import OpenAI


@lru_cache(maxsize=1)
def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)
