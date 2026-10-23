import os

from openai import OpenAI


def secret_audit_embedding(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
