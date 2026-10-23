import os

from openai import OpenAI


def embed_caption_chunks(chunks: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.embeddings.create(model="text-embedding-3-small", input=chunks)
    return [item.embedding for item in resp.data]
