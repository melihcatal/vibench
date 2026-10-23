import os
import openai
from typing import List, Dict, Any


def secret_audit_embedding(audit_notes: List[str], model: str = None) -> Dict[str, Any]:
    """Embed secret audit notes for semantic search using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    if model is None:
        model = "text-embedding-3-small"

    client = openai.OpenAI(api_key=api_key)

    embeddings = []
    for i, note in enumerate(audit_notes):
        if not note.strip():
            continue

        try:
            response = client.embeddings.create(
                model=model, input=note, encoding_format="float"
            )

            embedding_data = {
                "note_index": i,
                "note": note,
                "embedding": response.data[0].embedding,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
            embeddings.append(embedding_data)

        except Exception as e:
            error_data = {
                "note_index": i,
                "note": note,
                "error": str(e),
                "embedding": None,
            }
            embeddings.append(error_data)

    total_tokens = sum(
        emb.get("usage", {}).get("total_tokens", 0)
        for emb in embeddings
        if emb.get("usage")
    )

    successful_embeddings = [
        emb
        for emb in embeddings
        if emb.get("embedding") is not None and "error" not in emb
    ]

    return {
        "total_notes": len(audit_notes),
        "successful_embeddings": len(successful_embeddings),
        "failed_embeddings": len(audit_notes) - len(successful_embeddings),
        "total_tokens": total_tokens,
        "model": model,
        "embeddings": embeddings,
    }
