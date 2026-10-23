import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_batch(texts):
    response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [item.embedding for item in response.data]
