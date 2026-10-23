import os
from typing import List
from openai import OpenAI

def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=script
    )
    return [float(x) for x in response.data[0].embedding]  # Ensure list of float
