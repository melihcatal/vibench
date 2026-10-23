import os
from openai import OpenAI
from typing import List

def embed_script(script: str) -> List[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=script
    )
    return [float(x) for x in response.data[0].embedding]