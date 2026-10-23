import os

from openai import OpenAI


def main(text: str = "") -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return response.data[0].embedding
