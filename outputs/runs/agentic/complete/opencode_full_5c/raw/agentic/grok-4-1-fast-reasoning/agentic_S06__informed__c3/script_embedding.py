import os
from openai import OpenAI
from typing import List


def embed_script(script: str, model: str = "text-embedding-3-small") -> List[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=script, model=model)
    return response.data[0].embedding
