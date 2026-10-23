import os
from openai import OpenAI


def embed_platform_output(text: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
