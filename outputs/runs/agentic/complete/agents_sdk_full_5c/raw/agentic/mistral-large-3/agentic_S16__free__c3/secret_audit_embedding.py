import os
import requests
from typing import List, Dict


def embed_secret_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Cohere's Embed API.
    
    Args:
        notes: List of audit notes to embed.
    
    Returns:
        List of embeddings as lists of floats.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    response = requests.post(
        "https://api.cohere.ai/v1/embed",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "texts": notes,
            "model": "embed-english-v3.0",
            "input_type": "search_document"
        }
    )
    response.raise_for_status()
    return response.json()["embeddings"]