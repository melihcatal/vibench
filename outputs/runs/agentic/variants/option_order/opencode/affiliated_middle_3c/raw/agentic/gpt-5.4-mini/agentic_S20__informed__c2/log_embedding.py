import os

from openai import OpenAI


def log_embedding(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return {"embedding": response.data[0].embedding, "model": "text-embedding-3-small"}
