import os
from openai import OpenAI
from typing import List, Dict


def embed_secret_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using OpenAI's text-embedding-3-small model.
    
    Args:
        audit_notes: A list of audit notes (e.g., ["Rotation failed due to..."]).
    
    Returns:
        A list of embedding vectors for each audit note.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    
    client = OpenAI(api_key=openai_api_key)
    embeddings = []
    for note in audit_notes:
        response = client.embeddings.create(
            input=note,
            model="text-embedding-3-small"
        )
        embeddings.append(response.data[0].embedding)
    
    return embeddings