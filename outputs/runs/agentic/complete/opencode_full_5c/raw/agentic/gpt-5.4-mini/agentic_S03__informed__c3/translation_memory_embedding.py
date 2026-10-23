import os

from openai import OpenAI


def translation_memory_embedding(text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return response.data[0].embedding
