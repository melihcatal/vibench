import os
import cohere
from typing import List

def embed_secret_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embed secret audit notes for semantic search using Cohere Embed API.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=notes, model="embed-english-v3.0")
    return response.embeddings