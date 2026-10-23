import os
from openai import Embedding


def embed_text(text):
    client = Embedding(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.create(model="text-embedding-ada-002", input=text)
    return result.data[0].embedding
