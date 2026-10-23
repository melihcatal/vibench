import os

from openai import OpenAI


def moderation_reason_embedding(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return (
        client.embeddings.create(model="text-embedding-3-small", input=text)
        .data[0]
        .embedding
    )
