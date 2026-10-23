import os

from openai import OpenAI


def embed_caption_chunks(chunks: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks,
    )
    return [item.embedding for item in response.data]
