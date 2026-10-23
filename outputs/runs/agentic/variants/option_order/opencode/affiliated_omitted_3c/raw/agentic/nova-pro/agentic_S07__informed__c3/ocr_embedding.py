import os
from openai import OpenAI


def embed_text(text):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
