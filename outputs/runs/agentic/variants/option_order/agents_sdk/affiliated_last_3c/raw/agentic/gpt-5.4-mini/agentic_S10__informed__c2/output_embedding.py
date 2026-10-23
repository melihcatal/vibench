import os

from openai import OpenAI

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_output(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
