import os
from cohere import Client
from typing import List

def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    api_key = os.getenv('COHERE_API_KEY')
    co = Client(api_key)
    
    response = co.embed(
        model="embed-english-v3.0",
        texts=notes,
        input_type="search_document"
    )
    
    return response.embeddings
