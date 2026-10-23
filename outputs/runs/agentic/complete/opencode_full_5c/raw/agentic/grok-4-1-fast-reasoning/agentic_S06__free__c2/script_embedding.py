import os
from openai import OpenAI
from typing import List


def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=script, model="text-embedding-3-small")
    return response.data[0].embedding
