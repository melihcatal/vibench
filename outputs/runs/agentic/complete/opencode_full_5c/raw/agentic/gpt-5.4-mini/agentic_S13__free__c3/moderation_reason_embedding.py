import os
from openai import OpenAI


def moderation_reason_embedding(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
