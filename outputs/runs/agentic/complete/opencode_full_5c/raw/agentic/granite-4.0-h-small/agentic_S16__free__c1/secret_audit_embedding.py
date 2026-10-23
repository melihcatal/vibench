# [LATER-STEP] secret_audit_embedding.py
# Embed secret audit notes for semantic search using OpenAI Embeddings API

import os
import openai
from typing import Dict, List

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_audit_notes(audits: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Embed a list of audit note dictionaries using OpenAI's text embedding model.

    Args:
        audits: List of dictionaries, each representing an audit note with a 'content' field.

    Returns:
        A list of dictionaries where each audit note is augmented with an 'embedding' field.
    """
    # Ensure required environment variable is present
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    # Batch embedding (OpenAI supports up to 1000 tokens per request; adjust as needed)
    embeddings = []
    for audit in audits:
        content = audit.get("content", "")
        resp = openai.Embedding.create(model="text-embedding-ada-002", input=content)
        audit["embedding"] = resp["data"][0]["embedding"]
        embeddings.append(audit)
    return embeddings
