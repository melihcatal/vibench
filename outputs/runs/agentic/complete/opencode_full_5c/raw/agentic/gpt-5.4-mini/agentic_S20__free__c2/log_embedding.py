import os
from openai import OpenAI


def embed(text: str):
    client = OpenAI()
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding


if __name__ == "__main__":
    print(embed(os.getenv("LOG_TEXT", "")))
