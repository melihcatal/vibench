import os
from typing import List[float]

def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable required')
    import cohere
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[audit_notes],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]