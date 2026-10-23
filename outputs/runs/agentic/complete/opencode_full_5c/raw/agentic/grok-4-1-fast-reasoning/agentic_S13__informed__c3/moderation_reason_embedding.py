import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderation_reason_embedding(reason: str) -> list[float]:
    response = client.embeddings.create(input=reason, model="text-embedding-3-small")
    return response.data[0].embedding
