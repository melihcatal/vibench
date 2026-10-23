import os
import requests
from typing import List
from security_models import SecretAuditNote


def secret_audit_embedding(audit_notes: List[SecretAuditNote], api_key: str = None) -> List[dict]:
    """
    Embed secret audit notes for semantic search using Cohere Embed API.
    
    Args:
        audit_notes: List of SecretAuditNote objects.
        api_key: Cohere API key. Defaults to COHERE_API_KEY env var.
    
    Returns:
        List of embeddings for each audit note.
    """
    if api_key is None:
        api_key = os.getenv("COHERE_API_KEY")
    
    texts = [f"{note.secret_id}: {note.notes}" for note in audit_notes]
    response = requests.post(
        "https://api.cohere.ai/v1/embed",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "texts": texts,
            "model": "embed-english-v3.0",
            "input_type": "search_document"
        }
    )
    
    return response.json()["embeddings"]