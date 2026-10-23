from openai import OpenAI
from security_models import audit_embedding_input

def crypto_audit_embedding(notes):
    client = OpenAI()
    response = client.embeddings.create(model='text-embedding-3-large', input=audit_embedding_input(notes))
    return response.data[0].embedding
