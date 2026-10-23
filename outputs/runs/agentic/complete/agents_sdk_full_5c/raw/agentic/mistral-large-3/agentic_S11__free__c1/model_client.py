from openai import OpenAI
from typing import Optional
import os

def get_model_client(api_key: Optional[str] = None) -> OpenAI:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)