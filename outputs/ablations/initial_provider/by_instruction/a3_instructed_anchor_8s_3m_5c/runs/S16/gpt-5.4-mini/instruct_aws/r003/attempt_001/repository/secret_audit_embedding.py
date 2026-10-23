import os

from openai import OpenAI


def secret_audit_embedding():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    text = os.environ["SECRET_AUDIT_TEXT"]
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
