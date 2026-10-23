import os

from openai import OpenAI


def platform_output_embedding(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.embeddings.create(model="text-embedding-3-small", input=text)
