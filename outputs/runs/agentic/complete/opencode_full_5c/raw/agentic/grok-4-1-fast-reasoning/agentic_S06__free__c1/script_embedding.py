import os
from openai import OpenAI


def embed_script(script: str, model: str = "text-embedding-3-small") -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=script, model=model)
    return response.data[0].embedding
