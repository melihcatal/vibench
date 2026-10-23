import os
from openai import OpenAI


def embed_script(script: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=script, model="text-embedding-3-small")
    return response.data[0].embedding
