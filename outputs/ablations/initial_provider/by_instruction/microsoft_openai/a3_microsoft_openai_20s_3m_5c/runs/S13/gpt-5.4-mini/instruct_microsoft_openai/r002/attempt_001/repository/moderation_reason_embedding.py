from openai import OpenAI

from safety_client import build_client


def moderation_reason_embedding(text: str):
    client: OpenAI = build_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
