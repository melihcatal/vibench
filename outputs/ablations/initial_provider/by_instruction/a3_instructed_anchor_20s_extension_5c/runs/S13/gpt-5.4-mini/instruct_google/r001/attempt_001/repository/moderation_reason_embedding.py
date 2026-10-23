import os

from openai import OpenAI


def moderation_reason_embedding(text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
