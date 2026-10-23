import os

from openai import OpenAI


def embed_script(text, model=None):
    client = OpenAI()
    response = client.embeddings.create(
        model=model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        input=text,
    )
    return response.data[0].embedding if response.data else []
