import os

from openai import OpenAI


def embed_log_messages(texts: list[str]) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.embeddings.create(
        model="text-embedding-3-small", input=texts
    ).model_dump()
