import os

from openai import OpenAI


def embed_script(text: str) -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
