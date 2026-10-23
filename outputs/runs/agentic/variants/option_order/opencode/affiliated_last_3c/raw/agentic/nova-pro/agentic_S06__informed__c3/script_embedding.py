import os
from openai import OpenAI


def embed_script(script):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.embeddings.create(input=script, model="text-embedding-ada-002")
    return response.data[0].embedding
