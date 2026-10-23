import os
from openai import OpenAI
from typing import Dict, Any, List


def embed_crypto_audit_note(note: str) -> Dict[str, Any]:
    """
    Embeds crypto audit notes for semantic search using OpenAI Embeddings.
    
    Args:
        note: The audit note text to embed.
    
    Returns:
        A dictionary containing the embedding and metadata.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.embeddings.create(
        input=note,
        model="text-embedding-ada-002"
    )
    
    return {
        "embedding": response.data[0].embedding,
        "model": "text-embedding-ada-002",
        "provider": "openai",
        "text": note
    }