import openai
import os
from typing import List, Dict, Any

def embed_secret_audit_notes(
    audit_notes: List[str],
    model: str = "text-embedding-ada-002",
) -> List[Dict[str, Any]]:
    """
    Embeds secret audit notes using OpenAI Embeddings for semantic search.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = openai.OpenAI(api_key=openai_api_key)

    if not audit_notes:
        return []

    try:
        response = client.embeddings.create(
            input=audit_notes,
            model=model
        )
        embeddings_data = []
        for i, embedding_obj in enumerate(response.data):
            embeddings_data.append({
                "note": audit_notes[i],
                "embedding": embedding_obj.embedding,
                "index": embedding_obj.index
            })
        return embeddings_data
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error during embedding: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

