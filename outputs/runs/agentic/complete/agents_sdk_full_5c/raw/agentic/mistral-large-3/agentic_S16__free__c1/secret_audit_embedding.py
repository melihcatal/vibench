import os
from openai import OpenAI
from typing import List

def embed_secret_audit_notes(notes: List[str], api_key: str = None) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using OpenAI's text-embedding-ada-002.
    
    Args:
        notes: List of audit notes to embed.
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
    
    Returns:
        List of embeddings for each note.
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    client = OpenAI(api_key=api_key)
    embeddings = []
    
    for note in notes:
        response = client.embeddings.create(
            input=note,
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)
    
    return embeddings