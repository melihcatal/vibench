import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)
