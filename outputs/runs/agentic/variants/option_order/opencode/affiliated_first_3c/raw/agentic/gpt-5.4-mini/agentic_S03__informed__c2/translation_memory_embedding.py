import os

from openai import OpenAI


def translation_memory_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return list(response.data[0].embedding)
