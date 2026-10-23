import os

from openai import OpenAI


def embed_output(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding
