import os
from openai import OpenAI

def embed_secret_audit_notes(notes):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(input=notes, model='text-embedding-ada-002')
    return response.data[0].embedding