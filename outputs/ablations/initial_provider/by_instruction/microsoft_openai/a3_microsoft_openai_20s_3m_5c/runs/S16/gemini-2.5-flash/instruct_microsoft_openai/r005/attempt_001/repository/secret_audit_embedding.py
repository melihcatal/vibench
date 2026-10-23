import os
from security_client import get_openai_client

def embed_secret_audit_notes(notes: str) -> list[float]:
    client = get_openai_client()
    
    # OpenAI's recommended model for embeddings
    model = "text-embedding-ada-002"
    
    response = client.embeddings.create(input=notes, model=model)
    
    # The embedding is a list of floats
    embedding = response.data[0].embedding
    
    return embedding
