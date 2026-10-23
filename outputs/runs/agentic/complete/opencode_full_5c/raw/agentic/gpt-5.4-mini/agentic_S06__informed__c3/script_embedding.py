import os

from openai import OpenAI


def embed_script(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return (
        client.embeddings.create(model="text-embedding-3-large", input=text)
        .data[0]
        .embedding
    )
