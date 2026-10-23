import os
from openai import OpenAI
from typing import Optional

def get_embeddings_client(api_key: Optional[str] = None) -> OpenAI:
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    return OpenAI(api_key=api_key)