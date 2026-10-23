import os
from openai import OpenAI


def embed(text: str) -> list[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
