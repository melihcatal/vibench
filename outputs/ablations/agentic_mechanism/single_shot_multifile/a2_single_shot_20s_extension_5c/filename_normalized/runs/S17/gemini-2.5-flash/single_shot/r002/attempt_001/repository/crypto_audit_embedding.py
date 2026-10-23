import os
from typing import List, Dict, Any
import openai
from security_client import get_openai_client
from security_models import AuditNote

def embed_audit_notes(notes: List[str], model: str = "text-embedding-ada-002") -> List[Dict[str, Any]]:
    """Generates embeddings for a list of crypto audit notes using OpenAI's embedding API."""
    openai_client = get_openai_client()

    embeddings_list: List[Dict[str, Any]] = []
    if not notes:
        return embeddings_list

    try:
        response = openai_client.embeddings.create(
            input=notes,
            model=model
        )

        for i, embedding_data in enumerate(response.data):
            embeddings_list.append({
                "original_text": notes[i],
                "embedding": embedding_data.embedding,
                "model": model
            })

    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error generating embeddings: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings for audit notes: {e}")

    return embeddings_list