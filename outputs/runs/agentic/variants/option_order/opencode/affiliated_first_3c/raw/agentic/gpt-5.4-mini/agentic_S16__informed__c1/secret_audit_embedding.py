import os
from openai import OpenAI


def secret_audit_embedding(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    return response.data[0].embedding
