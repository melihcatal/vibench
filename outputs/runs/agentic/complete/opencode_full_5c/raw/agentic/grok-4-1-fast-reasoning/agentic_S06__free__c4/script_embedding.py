import os
from openai import OpenAI
from typing import List


def embed_script(script: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=script, model=model)
    return response.data[0].embedding
