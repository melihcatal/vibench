import os

from openai import OpenAI


def translation_memory_embedding(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    resp = client.embeddings.create(model="text-embedding-3-large", input=text)
    return resp.data[0].embedding
