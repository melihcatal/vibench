import os
from openai import Embedding

client = Embedding(api_key=os.getenv("OPENAI_API_KEY"))


def transcript_embedding(text):
    return client.create(input=text)["data"][0]["embedding"]
