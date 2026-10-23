import os
from openai import OpenAI
from typing import List, Dict

def embed_secret_audit_embedding(audit_notes: List[str]) -> Dict[str, List[float]]:
    """
    Embeds secret audit notes for semantic search using OpenAI.

    Args:
        audit_notes: A list of strings, where each string is an audit note.

    Returns:
        A dictionary mapping each note to its embedding vector.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    embeddings: Dict[str, List[float]] = {}

    try:
        response = client.embeddings.create(
            input=audit_notes,
            model="text-embedding-3-small"  # A specific, cost-effective OpenAI model
        )
        
        for i, note in enumerate(audit_notes):
            embeddings[note] = response.data[i].embedding
            
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return {}

    return embeddings
