import os
import google.generativeai as genai
from typing import List


def secret_audit_embedding(audit_notes: List[str]) -> List[List[float]]:
    """Embeds secret audit notes for semantic search using Google Gemini Embeddings.

    Args:
        audit_notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors, one for each audit note.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    embeddings = genai.embed_content(
        model="models/embedding-001",
        content=audit_notes,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return embeddings["embedding"]
