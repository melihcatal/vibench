import os
from openai import Embedding


def embed_text(text):
    api_key = os.getenv("OPENAI_API_KEY")
    embedding = Embedding(api_key)
    result = embedding.create(input=text, model="text-embedding-ada-002")
    return result.data[0].embedding
