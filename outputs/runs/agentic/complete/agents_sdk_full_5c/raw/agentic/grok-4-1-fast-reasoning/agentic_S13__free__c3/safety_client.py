import os
from typing import Optional
from openai import OpenAI

_client: Optional[OpenAI] = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('OPENAI_API_KEY environment variable is required.')
        _client = OpenAI(api_key=api_key)
    return _client
