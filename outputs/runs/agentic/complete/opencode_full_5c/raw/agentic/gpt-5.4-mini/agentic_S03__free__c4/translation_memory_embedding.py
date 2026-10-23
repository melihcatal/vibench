import os

from openai import OpenAI


def translation_memory_embedding(segment: str) -> list[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=segment)
    return response.data[0].embedding
