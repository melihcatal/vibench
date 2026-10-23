import cohere
import os
from typing import List

def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embeds crypto audit notes for semantic search using Cohere Embed API.
    """
    co = cohere.Client(os.getenv('COHERE_API_KEY'))
    response = co.embed(
        texts=notes,
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return [embedding for embedding in response.embeddings]
